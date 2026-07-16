from src.infrastructure.real.mcp_server.tools.vector_search.embedding.tei_embedding_adapter import TeiEmbeddingAdapter
from src.infrastructure.real.mcp_server.tools.vector_search.qdrant_vector_store_adapter import QdrantVectorStoreAdapter
from src.infrastructure.real.mcp_server.tools.vector_search.vector_search_tool import VectorSearchTool


class VectorSearchInfrasture:
    def __init__(self):
        self.vector_store = None
        self.embedder = None
        self.tool = None

    def build(self) -> VectorSearchTool:
        from src.infrastructure.config.settings import settings
        from src.infrastructure.config.seed_data import SEED_DATA
        from src.infrastructure.config.vector_seeder import VectorSeeder
        from src.infrastructure.real.mcp_server.tools.vector_search.faiss_vector_store import FaissVectorStore
        from src.infrastructure.real.mcp_server.tools.vector_search.vector_search_tool import VectorSearchTool

        self.vector_store = QdrantVectorStoreAdapter(url=settings.qdrant_target_address)

        self.embedder = TeiEmbeddingAdapter(
            target_url=settings.embedding_target_address
        )

        seeder = VectorSeeder(
            vector_store=self.vector_store,
            embedder=self.embedder
        )

        seeder.reset_and_seed(SEED_DATA)

        self.tool = VectorSearchTool(
            vector_store=self.vector_store,
            embedder=self.embedder
        )

        return self.tool