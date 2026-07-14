import asyncio
import time

from src.domain.query import Query
from src.infrastructure.real.http.real_http_client import RealHttpClient
from src.infrastructure.real.mcp_server.tools.core.tool_information import WEB_SEARCH_TOOL
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
# from src.infrastructure.real.mcp_server.tools.web_search.http_web_search_client import HttpWebSearchClient
from src.infrastructure.real.mcp_server.tools.web_search.mock_web_search_client import MockWebSearchClient
from src.infrastructure.real.mcp_server.tools.web_search.web_search_tool import WebSearchTool

"""
End-to-end test for WebSearchTool.

Verifies that a query is executed through the full pipeline
and measures the total execution time.
"""

http_client = RealHttpClient()
web_search_client = MockWebSearchClient()
web_search = WebSearchTool(web_search_client)

query = "Is the stock market up or down today?"

tool_request = ToolRequest(
    tool_name=WEB_SEARCH_TOOL.name,
    params={
        ToolIOKeys.QUERY: Query(text=query)
    }
)


async def call_tool():
    start = time.perf_counter()

    response = await web_search.execute(tool_request)

    end = time.perf_counter()

    print(response)
    print(f"\nExecution Time: {end - start:.3f} seconds")


if __name__ == "__main__":
    asyncio.run(call_tool())