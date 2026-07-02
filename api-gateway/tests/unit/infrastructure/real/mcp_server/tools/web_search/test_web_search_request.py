import pytest  # type: ignore

from src.domain.query import Query
from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.web_search.web_search_request import WebSearchRequest


# -------------------------
# SUCCESS CASE
# -------------------------
def test_web_search_request_create_success():

    base_request = ToolRequest(
        tool_name=ToolName("WEB_SEARCH_TOOL"),
        params={
            ToolIOKeys.QUERY: Query("what is ai")
        }
    )

    web_request = WebSearchRequest.create(base_request)

    assert isinstance(web_request, WebSearchRequest)
    assert web_request.tool_name == base_request.tool_name
    assert web_request.query.text == Query("what is ai").text
    assert web_request.params == base_request.params


# -------------------------
# MISSING QUERY ERROR
# -------------------------
def test_web_search_request_missing_query_raises():

    base_request = ToolRequest(
        tool_name=ToolName("WEB_SEARCH_TOOL"),
        params={}
    )

    with pytest.raises(ValueError) as e:  # type: ignore[misc]
        WebSearchRequest.create(base_request)

    assert "cannot be called without query" in str(e.value) # type: ignore


# -------------------------
# PARAMS PRESERVED
# -------------------------
def test_web_search_request_preserves_params():

    base_request = ToolRequest(
        tool_name=ToolName("WEB_SEARCH_TOOL"),
        params={
            ToolIOKeys.QUERY: Query("test query"),
            ToolIOKeys.METADATA: {"lang": "en"}
        }
    )

    result = WebSearchRequest.create(base_request)

    assert ToolIOKeys.QUERY in result.params
    assert ToolIOKeys.METADATA in result.params