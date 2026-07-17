import uuid
import traceback
from typing import List, Dict, Any

# 1. CRITICAL: Import the Async client!
from qdrant_client import AsyncQdrantClient 
from qdrant_client.models import PointStruct, VectorParams, Distance
from qdrant_client.http.exceptions import UnexpectedResponse

from src.infrastructure.real.mcp_server.tools.vector_search.vector_store_port import VectorStorePort


class QdrantVectorStoreAdapter(VectorStorePort):
    def __init__(
        self, 
        url: str, 
        collection_name: str = "orion_mcp_collection",
        vector_size: int = 384,
        distance_metric: Distance = Distance.COSINE
    ):
        # 2. Use AsyncQdrantClient
        self.client = AsyncQdrantClient(url=url)
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.distance_metric = distance_metric
        
        # NOTE: We cannot call 'await self._ensure_collection_exists()' inside __init__ 
        # because __init__ cannot be async. You will need to call this method once 
        # when your application starts up!

    async def _ensure_collection_exists(self) -> None:
        try:
            await self.client.get_collection(collection_name=self.collection_name)
        except (UnexpectedResponse, ValueError):
            await self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size, 
                    distance=self.distance_metric
                ),
            )

    def _get_deterministic_uuid(self, doc_id: str) -> str:
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, doc_id))

    # 3. Add 'async def' to all methods that make network calls
    async def add(self, doc_id: str, vector: List[float]) -> None:
        point_id = self._get_deterministic_uuid(doc_id)
        
        await self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload={"original_doc_id": doc_id}
                )
            ]
        )

    async def add_batch(self, doc_ids: List[str], vectors: List[List[float]]) -> None:
        if len(doc_ids) != len(vectors):
            raise ValueError("The lengths of doc_ids and vectors must perfectly match.")

        points = [
            PointStruct(
                id=self._get_deterministic_uuid(doc_id),
                vector=vec,
                payload={"original_doc_id": doc_id}
            )
            for doc_id, vec in zip(doc_ids, vectors)
        ]

        await self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    async def search(
        self,
        query_vector: Any, 
        k: int = 5
    ) -> List[Dict[str, Any]]:
        
        clean_query = query_vector.tolist() if hasattr(query_vector, "tolist") else list(query_vector)

        try:
            response = await self.client.query_points(
                collection_name=self.collection_name,
                query=clean_query,
                limit=k,
                with_payload=True 
            )
            
            search_results = response.points

            return [
                {
                    "doc_id": hit.payload.get("original_doc_id", str(hit.id)),
                    "score": hit.score
                }
                for hit in search_results
            ]

        except Exception as e:
            traceback.print_exc() 
            return []
    
    async def reset(self) -> None:
        try:
            await self.client.delete_collection(collection_name=self.collection_name)
        except UnexpectedResponse:
            pass 
        
        await self._ensure_collection_exists()