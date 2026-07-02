import pytest  # type: ignore

from src.domain.query import Query
from src.domain.tool_name import ToolName
from src.infrastructure.real.http.http_client_port import HttpClientPort
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.web_search.web_search_tool import WebSearchTool
from src.infrastructure.real.http.http_response import HttpResponse


# -------------------------
# FAKE HTTP CLIENT
# -------------------------from src.infrastructure.real.http.http_client_port import HttpClientPort
from src.infrastructure.real.http.http_response import HttpResponse


class FakeHttpClient(HttpClientPort):

    async def get(self, url, headers=None, params=None, timeout=None):  # type: ignore
        raise NotImplementedError()

    async def post(self, url, data=None, json=None, headers=None, timeout=None):  # type: ignore
        return HttpResponse(
            status_code=200,
            headers={},
            body={
                "query": json["query"], # type: ignore
                "results": [
                    {
                        "title": "AI News",
                        "url": "https://example.com/ai",
                        "content": "AI is transforming the world",
                        "score": 0.95
                    }
                ],
                "answer": "AI summary"
            }
        )

    async def put(self, url, data=None, json=None, headers=None, timeout=None):  # type: ignore
        raise NotImplementedError()

    async def delete(self, url, headers=None, timeout=None):  # type: ignore
        raise NotImplementedError()


# -------------------------
# TEST SUCCESS PATH
# -------------------------
@pytest.mark.asyncio  # type: ignore[misc]
async def test_web_search_tool_execute_success():

    tool = WebSearchTool(http_client=FakeHttpClient())

    tool_request = ToolRequest(
        tool_name=ToolName("WEB_SEARCH_TOOL"),
        params={
            ToolIOKeys.QUERY: Query("what is ai")
        }
    )

    result = await tool.execute(tool_request)

    # -------------------------
    # BASIC STRUCTURE
    # -------------------------
    assert result.tool_name == ToolName("WEB_SEARCH_TOOL")
    assert result.success is True

    # -------------------------
    # OUTPUT EXISTS
    # -------------------------
    assert ToolIOKeys.WEB_RESULTS in result.output

    results = result.output[ToolIOKeys.WEB_RESULTS]

    # -------------------------
    # RESULT CONTENT CHECK
    # -------------------------
    assert isinstance(results.results, list)
    assert len(results.results) == 1 # type: ignore

    first = results.results[0] # type: ignore
    print('adsf', first) # type: ignore
    assert first.title == "AI News" # type: ignore
    assert first.url == "https://example.com/ai" # type: ignore
    assert first.snippet == "AI is transforming the world" # type: ignore
    assert first.score == 0.95 # type: ignore


# -------------------------
# INVALID REQUEST (missing query)
# -------------------------
def test_web_search_tool_missing_query_raises():

    tool = WebSearchTool(http_client=FakeHttpClient())

    tool_request = ToolRequest(
        tool_name=ToolName("WEB_SEARCH_TOOL"),
        params={}
    )

    with pytest.raises(ValueError) as e:  # type: ignore[misc]
        import asyncio
        asyncio.run(tool.execute(tool_request))

    assert "query" in str(e.value) # type: ignore