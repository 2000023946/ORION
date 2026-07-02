import asyncio

from src.domain.query import Query
from src.infrastructure.real.http.real_http_client import RealHttpClient
from src.infrastructure.real.mcp_server.tools.core.tool_information import WEB_SEARCH_TOOL
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.web_search.web_search_tool import WebSearchTool
"""
End-to-end test for WebSearchTool.

Verifies that a query is executed through the full pipeline
and returns a valid ToolResponse.
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