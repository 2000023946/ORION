import pytest  # type: ignore

from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.vector_search.doc_id import DocId
from src.infrastructure.real.mcp_server.tools.metadata_filter.metadata_filter_request import (
    MetadataFilterRequest,
)


# -------------------------
# SUCCESS CASE
# -------------------------
def test_metadata_filter_request_create_success():

    base_request = ToolRequest(
        tool_name=ToolName("METADATA_FILTER_TOOL"),
        params={
            ToolIOKeys.DOCS_IDS: [
                DocId("a"),
                DocId("b"),
            ]
        }
    )

    result = MetadataFilterRequest.create(base_request)

    assert isinstance(result, MetadataFilterRequest)
    assert result.tool_name == base_request.tool_name
    assert len(result.docs_ids) == 2
    assert result.docs_ids[0] == DocId("a")


# -------------------------
# MISSING DOCS_IDS ERROR
# -------------------------
def test_metadata_filter_request_missing_docs_ids():

    base_request = ToolRequest(
        tool_name=ToolName("METADATA_FILTER_TOOL"),
        params={}
    )

    with pytest.raises(ValueError) as e:  # type: ignore[misc]
        MetadataFilterRequest.create(base_request)

    assert "DOCS_IDS" in str(e.value)


# -------------------------
# SERIALIZE IDS
# -------------------------
def test_metadata_filter_request_serialize_ids():

    request = MetadataFilterRequest(
        tool_name=ToolName("METADATA_FILTER_TOOL"),
        docs_ids=[
            DocId("x"),
            DocId("y"),
        ],
        params={}
    )

    result = request.serialize_ids()

    assert result == ["x", "y"]


# -------------------------
# PARAMS PRESERVED
# -------------------------
def test_metadata_filter_request_params_preserved():

    base_request = ToolRequest(
        tool_name=ToolName("METADATA_FILTER_TOOL"),
        params={
            ToolIOKeys.DOCS_IDS: [DocId("1")]
        }
    )

    result = MetadataFilterRequest.create(base_request)

    assert ToolIOKeys.DOCS_IDS in result.params
    assert result.params[ToolIOKeys.DOCS_IDS][0].doc_id == "1"