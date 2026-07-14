
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_port import ToolPort
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.web_search.web_search_client import WebSearchClient
from src.infrastructure.real.mcp_server.tools.web_search.web_search_request import WebSearchRequest
from src.ports.tool_response import ToolResponse


class WebSearchTool(ToolPort):

    def __init__(self, web_search_client: WebSearchClient):
        self.web_search_client = web_search_client

    async def execute(self, tool_request: ToolRequest) -> ToolResponse:

        # ----------------------------
        # 1. Build typed request
        # ----------------------------
        request = WebSearchRequest.create(tool_request)
        print("making a web search with qeury", request.query.text)
        # ----------------------------
        # 2. Call external API
        # ----------------------------
        
        web_search_response = await self.web_search_client.search(query=request.query)

        # ----------------------------
        # 4. Return standardized ToolResponse
        # ----------------------------
        return ToolResponse(
            tool_name=tool_request.tool_name,
            output={
                ToolIOKeys.WEB_RESULTS: web_search_response
            },
            success=True
        )