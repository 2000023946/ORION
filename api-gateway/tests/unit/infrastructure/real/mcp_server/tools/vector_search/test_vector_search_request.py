import pytest  # type: ignore

from src.domain.query import Query
from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.vector_search.vector_search_request import VectorSearchRequest


# -------------------------
# SUCCESS CASE
# -------------------------
def test_vector_search_request_create_success():

    base_request = ToolRequest(
        tool_name=ToolName("VECTOR_SEARCH_TOOL"),
        params={
            ToolIOKeys.QUERY: Query("find similar docs")
        }
    )

    result = VectorSearchRequest.create(base_request)

    assert isinstance(result, VectorSearchRequest)
    assert result.tool_name == base_request.tool_name
    assert result.query.text == Query("find similar docs").text
    assert result.params == base_request.params


# -------------------------
# MISSING QUERY ERROR
# -------------------------
def test_vector_search_request_missing_query_raises():

    base_request = ToolRequest(
        tool_name=ToolName("VECTOR_SEARCH_TOOL"),
        params={}
    )

    with pytest.raises(ValueError) as e:  # type: ignore[misc]
        VectorSearchRequest.create(base_request)

    assert "query param" in str(e.value) # type: ignore


# -------------------------
# PARAMS PRESERVED
# -------------------------
def test_vector_search_request_preserves_params():

    base_request = ToolRequest(
        tool_name=ToolName("VECTOR_SEARCH_TOOL"),
        params={
            ToolIOKeys.QUERY: Query("test"),
            ToolIOKeys.METADATA: {"source": "unit-test"}
        }
    )

    result = VectorSearchRequest.create(base_request)

    assert ToolIOKeys.QUERY in result.params
    assert ToolIOKeys.METADATA in result.params