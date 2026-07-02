import pytest  # type: ignore

from src.domain.query import Query
from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.vector_search.vector_search_tool import VectorSearchTool


# -------------------------
# FAKE EMBEDDER
# -------------------------
class FakeEmbedder:

    def embed(self, text: str):
        # deterministic vector
        return [0.1, 0.2, 0.3]


# -------------------------
# FAKE VECTOR STORE
# -------------------------
class FakeVectorStore:

    def search(self, query_vector, k):
        return [
            {"doc_id": "doc1", "score": 0.95},
            {"doc_id": "doc2", "score": 0.80},
        ]


# -------------------------
# TEST SUCCESS CASE
# -------------------------
@pytest.mark.asyncio  # type: ignore[misc]
async def test_vector_search_tool_success():

    tool = VectorSearchTool(
        vector_store=FakeVectorStore(),
        embedder=FakeEmbedder()
    )

    tool_request = ToolRequest(
        tool_name=ToolName("VECTOR_SEARCH_TOOL"),
        params={
            ToolIOKeys.QUERY: Query("find similar docs")
        }
    )

    result = await tool.execute(tool_request)

    # -------------------------
    # BASIC STRUCTURE
    # -------------------------
    assert result.tool_name == ToolName("VECTOR_SEARCH_TOOL")
    assert result.success is True

    # -------------------------
    # OUTPUT CHECK
    # -------------------------
    assert ToolIOKeys.DOCS_IDS in result.output

    docs = result.output[ToolIOKeys.DOCS_IDS]

    assert isinstance(docs, list)
    assert len(docs) == 2

    assert docs[0]["id"] == "doc1"
    assert docs[0]["score"] == 0.95


# -------------------------
# EMBEDDER CALLED CORRECTLY
# -------------------------
@pytest.mark.asyncio  # type: ignore[misc]
async def test_vector_search_tool_embedding_used():

    class SpyEmbedder:

        def __init__(self):
            self.called_with = None

        def embed(self, text: str):
            self.called_with = text
            return [0.1, 0.2]

    tool = VectorSearchTool(
        vector_store=FakeVectorStore(),
        embedder=SpyEmbedder()
    )

    tool_request = ToolRequest(
        tool_name=ToolName("VECTOR_SEARCH_TOOL"),
        params={
            ToolIOKeys.QUERY: Query("my query text")
        }
    )

    await tool.execute(tool_request)

    assert tool.embedder.called_with == "my query text"


# -------------------------
# VECTOR STORE CALL VALIDATION
# -------------------------
@pytest.mark.asyncio  # type: ignore[misc]
async def test_vector_store_called():

    class SpyStore:

        def __init__(self):
            self.called_with = None

        def search(self, query_vector, k):
            self.called_with = (query_vector, k)
            return [{"doc_id": "a", "score": 1.0}]

    tool = VectorSearchTool(
        vector_store=SpyStore(),
        embedder=FakeEmbedder()
    )

    tool_request = ToolRequest(
        tool_name=ToolName("VECTOR_SEARCH_TOOL"),
        params={
            ToolIOKeys.QUERY: Query("hello")
        }
    )

    await tool.execute(tool_request)

    vec, k = tool.vector_store.called_with

    assert vec == [0.1, 0.2, 0.3]
    assert isinstance(k, int)


# -------------------------
# INVALID REQUEST (missing query)
# -------------------------
def test_vector_search_tool_missing_query():

    tool = VectorSearchTool(
        vector_store=FakeVectorStore(),
        embedder=FakeEmbedder()
    )

    tool_request = ToolRequest(
        tool_name=ToolName("VECTOR_SEARCH_TOOL"),
        params={}
    )

    import asyncio

    with pytest.raises(ValueError):
        asyncio.run(tool.execute(tool_request))