from typing import List, Dict, Any

from src.infrastructure.real.mcp_server.tools.vector_search.embedding_port import EmbeddingPort
from src.infrastructure.real.mcp_server.tools.vector_search.vector_store_port import VectorStorePort




class VectorSeeder:
    """
    Resets vector store and seeds it with fresh embeddings.
    """

    def __init__(
        self,
        vector_store: VectorStorePort,
        embedder: EmbeddingPort
    ) -> None:
        self.vector_store = vector_store
        self.embedder = embedder

    def _to_text(self, item: Dict[str, Any]) -> str:
        return f"{item['title']} {item['content']}"

    def reset_and_seed(self, data: List[Dict[str, Any]]) -> None:
        """
        Clears vector store and rebuilds from scratch.
        """

        # 1. clear old vectors
        self.vector_store.reset()

        doc_ids: List[str] = []
        vectors: List[List[float]] = []

        # 2. embed + prepare batch
        for item in data:
            text = self._to_text(item)
            vector = self.embedder.embed(text)

            doc_ids.append(item["_id"])
            vectors.append(vector)

        # 3. bulk insert
        self.vector_store.add_batch(doc_ids, vectors)