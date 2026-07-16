import uuid
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from qdrant_client.http.exceptions import UnexpectedResponse
from src.infrastructure.real.mcp_server.tools.vector_search.vector_store_port import VectorStorePort

# Assuming VectorStorePort is imported from your ports module
# from your_project.ports import VectorStorePort

class QdrantVectorStoreAdapter(VectorStorePort):
    """
    Qdrant implementation of the VectorStorePort driving a remote Qdrant database service.
    """

    def __init__(
        self, 
        url: str, 
        collection_name: str = "orion_mcp_collection",
        vector_size: int = 384,  # Matches sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
        distance_metric: Distance = Distance.COSINE
    ):
        """
        Initializes the client and ensures the target collection exists.
        """
        self.client = QdrantClient(url=url)
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.distance_metric = distance_metric
        
        self._ensure_collection_exists()

    def _ensure_collection_exists(self) -> None:
        """
        Idempotent helper to initialize the collection schema if it does not exist.
        """
        try:
            # Check if collection exists
            self.client.get_collection(collection_name=self.collection_name)
        except (UnexpectedResponse, ValueError):
            # Create collection if missing
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size, 
                    distance=self.distance_metric
                ),
            )

    def _get_deterministic_uuid(self, doc_id: str) -> str:
        """
        Converts an arbitrary string doc_id into a valid 128-bit RFC 4122 UUID string 
        required by Qdrant's point ID specification.
        """
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, doc_id))

    def add(self, doc_id: str, vector: List[float]) -> None:
        """
        Adds a single vector to the Qdrant collection.
        """
        point_id = self._get_deterministic_uuid(doc_id)
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload={"original_doc_id": doc_id}
                )
            ]
        )

    def add_batch(self, doc_ids: List[str], vectors: List[List[float]]) -> None:
        """
        Optimized batch upsert for high-throughput enterprise loading.
        """
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

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(
        self,
        query_vector: List[float],
        k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Searches the collection and unwraps the payload to return the original doc_id.
        """
        search_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=k,
            with_payload=True  # Ensure payload is fetched to recover string ID
        )

        return [
            {
                # Recover the original string ID if present, fallback to point ID
                "doc_id": hit.payload.get("original_doc_id", str(hit.id)),
                "score": hit.score
            }
            for hit in search_results
        ]

    def reset(self) -> None:
        """
        Deletes the collection and immediately recreates it to clear state cleanly.
        """
        try:
            self.client.delete_collection(collection_name=self.collection_name)
        except UnexpectedResponse:
            pass  # Already missing or cleared
        
        self._ensure_collection_exists()