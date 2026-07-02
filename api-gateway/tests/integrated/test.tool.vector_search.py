import asyncio

from src.domain.query import Query
from src.infrastructure.config.seed_data import SEED_DATA
from src.infrastructure.config.settings import settings
from src.infrastructure.config.vector_seeder import VectorSeeder

from src.infrastructure.real.mcp_server.tools.core.tool_information import VECTOR_SEARCH_TOOL
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest

from src.infrastructure.real.mcp_server.tools.vector_search.faiss_vector_store import FaissVectorStore
from src.infrastructure.real.mcp_server.tools.vector_search.sentence_transformer_embedding import SentenceTransformerEmbedding
from src.infrastructure.real.mcp_server.tools.vector_search.vector_search_tool import VectorSearchTool


# ----------------------------
# Setup vector system
# ----------------------------

vector_store = FaissVectorStore(dim=settings.vector_db_dim)

embedder = SentenceTransformerEmbedding(
    model_name=settings.embedding_model
)

seeder = VectorSeeder(
    vector_store=vector_store,
    embedder=embedder
)

print("Initialized !!!")

seeder.reset_and_seed(SEED_DATA)

print("Data is seeded!")


# ----------------------------
# Build tool
# ----------------------------

vector_tool = VectorSearchTool(
    vector_store=vector_store,
    embedder=embedder
)


# ----------------------------
# Test query
# ----------------------------

QUERY_TEXT = "apple noise cancelling headphones"


tool_request = ToolRequest(
    tool_name=VECTOR_SEARCH_TOOL.name,
    params={
        ToolIOKeys.QUERY: Query(text=QUERY_TEXT)
    }
)


# ----------------------------
# Run test
# ----------------------------

async def main() -> None:
    response = await vector_tool.execute(tool_request)
    print("\n=== VECTOR SEARCH RESPONSE ===\n")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())