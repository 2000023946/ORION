import asyncio

from src.domain.query import Query
from src.infrastructure.real.http.real_http_client import RealHttpClient
from src.infrastructure.real.mcp_server.tools.core.tool_information import WEB_SEARCH_TOOL
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.web_search.web_search_tool import WebSearchTool

"""
Integrated Web Search Tool Test

Purpose
-------
This script performs an end-to-end integration test of the WebSearchTool.
It verifies that the entire pipeline works correctly, including:

    Query
        ↓
    ToolRequest
        ↓
    WebSearchTool
        ↓
    RealHttpClient
        ↓
    Tavily API
        ↓
    WebSearchResponse
        ↓
    ToolResponse

Expected Output
---------------
A successful run should print a ToolResponse similar to:

ToolResponse(
    success=True,
    output={
        WEB_RESULTS: WebSearchResponse(
            query="Is the stock market up or down today?",
            results=[
                WebSearchResult(...),
                ...
            ]
        )
    }
)

The exact search results will change over time.

What Success Looks Like
-----------------------
✓ success=True

✓ The query matches the one sent.

✓ results contains one or more WebSearchResult objects.

✓ Each result has:
    - title
    - url
    - snippet
    - score

Common Problems
---------------
results=[]

    • API key is invalid or missing.
    • Search request failed.
    • Query was not sent correctly.

query=""

    • The query was lost while constructing the request or parsing
      the response.

success=False

    • Network error.
    • HTTP error.
    • Exception thrown inside WebSearchTool.

Exceptions

    • Usually indicate a bug in the tool implementation,
      HTTP client, or response parser.

This file is intended only as a manual integration test and should not
be used as a unit test.
"""

http_client = RealHttpClient()
web_search = WebSearchTool(http_client)

query = "Is the stock market up or down today?"

tool_request = ToolRequest(
    tool_name=WEB_SEARCH_TOOL.name,
    params={
        ToolIOKeys.QUERY: Query(text=query)
    }
)


async def call_tool():
    response = await web_search.execute(tool_request)
    print(response)


if __name__ == "__main__":
    asyncio.run(call_tool())