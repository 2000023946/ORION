import uuid
import time
import logging

import httpx
from typing import Optional
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from qdrant_client.http.exceptions import UnexpectedResponse

from src.application.bus.search_task_response import SearchTaskResponse
from src.application.bus.request_id import RequestID
from src.domain.search_answer import SearchAnswer
from src.domain.query import Query
from src.ports.cache import CachePort
from src.infrastructure.config.settings import settings

logger = logging.getLogger(__name__)


class QdrantCacheAdapter(CachePort):
    def __init__(
        self,
        qdrant_client: AsyncQdrantClient,
        embedding_target_address: str = settings.embedding_target_address,
        collection_name: str = "semantic_cache",
        score_threshold: float = 0.92,
        vector_dim: int = settings.vector_db_dim,
        http_client: Optional[httpx.AsyncClient] = None,
    ):
        """
        Args:
            qdrant_client: Asynchronous Qdrant client instance.
            embedding_target_address: TEI / Embedding service HTTP URL.
            collection_name: Qdrant collection used exclusively for edge caching.
            score_threshold: Cosine similarity threshold (0.90 - 0.95 recommended).
            vector_dim: Dimensionality of the embedding model output.
            http_client: Optional shared httpx.AsyncClient for connection pooling.
                If not provided, one is created and owned by this adapter.
        """
        self.qdrant = qdrant_client
        self.embedding_url = embedding_target_address.rstrip("/")
        self.collection_name = collection_name
        self.score_threshold = score_threshold
        self.vector_dim = vector_dim
        self._collection_initialized = False
        self._owns_http_client = http_client is None
        self._http_client = http_client or httpx.AsyncClient(timeout=3.0)

    async def aclose(self) -> None:
        """Closes the owned HTTP client, if this adapter created it."""
        if self._owns_http_client:
            await self._http_client.aclose()

    async def _ensure_collection(self) -> None:
        """Lazily verifies or creates the semantic cache collection in Qdrant."""
        if self._collection_initialized:
            return

        exists = await self.qdrant.collection_exists(self.collection_name)
        if not exists:
            try:
                await self.qdrant.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.vector_dim,
                        distance=models.Distance.COSINE,
                    ),
                )
            except UnexpectedResponse as exc:
                # Another coroutine/process created it concurrently between
                # our exists-check and create call — safe to ignore.
                if "already exists" not in str(exc).lower():
                    raise

        self._collection_initialized = True

    async def _get_embedding(self, text: str) -> list[float]:
        """Fetches vector embedding for the query from the TEI microservice."""
        response = await self._http_client.post(
            f"{self.embedding_url}/embed",
            json={"inputs": text},
        )
        response.raise_for_status()
        data = response.json()

        # TEI returns a nested list [[0.1, 0.2, ...]] or single list [0.1, ...]
        if isinstance(data, list) and len(data) > 0:
            return data[0] if isinstance(data[0], list) else data

        raise ValueError(f"Unexpected embedding payload structure: {data}")

    async def get_answer(self, query: Query) -> Optional[SearchTaskResponse]:
        try:
            await self._ensure_collection()
            query_vector = await self._get_embedding(query.text)

            response = await self.qdrant.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=1,
                score_threshold=self.score_threshold,
                with_payload=True,
            )
            results = response.points
        except (httpx.HTTPError, UnexpectedResponse) as exc:
            # Cache should degrade gracefully rather than break the request path.
            logger.warning("Semantic cache lookup failed, treating as miss: %s", exc)
            return None

        if not results:
            return None

        match = results[0]
        data = dict(match.payload.get("response_data", {}))

        req_id_val = data.get("request_id")
        if req_id_val is not None:
            data["request_id"] = RequestID(value=req_id_val)

        answer_val = data.get("answer")
        data["answer"] = SearchAnswer(answer=answer_val) if answer_val else None

        return SearchTaskResponse(**data)

    async def set_answer(self, query: Query, response: SearchTaskResponse) -> None:
        try:
            await self._ensure_collection()
            query_vector = await self._get_embedding(query.text)

            # Deterministic UUID derived from query text so re-searches update rather than duplicate.
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, query.text.lower().strip()))

            await self.qdrant.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=point_id,
                        vector=query_vector,
                        payload={
                            "query_text": query.text,
                            "response_data": response.to_dict(),
                            "created_at": int(time.time()),
                        },
                    )
                ],
            )
        except (httpx.HTTPError, UnexpectedResponse) as exc:
            # Writing to the cache is best-effort; don't let it break the caller.
            logger.warning("Semantic cache write failed: %s", exc)