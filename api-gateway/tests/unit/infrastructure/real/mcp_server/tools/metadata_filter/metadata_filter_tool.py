import pytest  # type: ignore
from unittest.mock import MagicMock

from src.infrastructure.real.mcp_server.tools.metadata_filter.metadata_filter_tool import MetadataFilterTool
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.vector_search.doc_id import DocId


# -------------------------
# helper
# -------------------------
class FakeHttpClient:
    async def post(self, *args, **kwargs):
        return MagicMock(
            require=lambda key: [
                {
                    "_id": "1",
                    "title": "doc1",
                    "content": "hello",
                    "metadata": {"a": 1},
                },
                {
                    "_id": "2",
                    "title": "doc2",
                    "content": "world",
                    "metadata": {"b": 2},
                },
            ]
        )


# -------------------------
# SUCCESS CASE
# -------------------------
@pytest.mark.asyncio
async def test_metadata_filter_success():

    http_client = FakeHttpClient()
    tool = MetadataFilterTool(http_client)

    tool_request = ToolRequest(
        tool_name=ToolName("METADATA_FILTER_TOOL"),
        params={
            ToolIOKeys.DOCS_IDS: [
                DocId("1"),
                DocId("2"),
            ]
        }
    )

    result = await tool.execute(tool_request)

    assert result.success is True
    assert ToolIOKeys.DOCUMENTS in result.output

    docs = result.output[ToolIOKeys.DOCUMENTS]

    assert len(docs) == 2
    assert docs[0]["id"] == "1"
    assert docs[0]["title"] == "doc1"


# -------------------------
# EMPTY RESPONSE CASE
# -------------------------
@pytest.mark.asyncio
async def test_metadata_filter_empty():

    http_client = FakeHttpClient()

    # override response to empty
    http_client.post = MagicMock(
        return_value=MagicMock(
            require=lambda key: []
        )
    )

    tool = MetadataFilterTool(http_client)

    tool_request = ToolRequest(
        tool_name=ToolName("METADATA_FILTER_TOOL"),
        params={
            ToolIOKeys.DOCS_IDS: []
        }
    )

    result = await tool.execute(tool_request)

    assert result.success is True
    assert result.output[ToolIOKeys.DOCUMENTS] == []


# -------------------------
# VALIDATION ERROR CASE
# -------------------------
@pytest.mark.asyncio
async def test_metadata_filter_missing_docs_ids():

    http_client = FakeHttpClient()
    tool = MetadataFilterTool(http_client)

    tool_request = ToolRequest(
        tool_name=ToolName("METADATA_FILTER_TOOL"),
        params={}  # missing DOCS_IDS
    )

    with pytest.raises(ValueError):
        await tool.execute(tool_request)