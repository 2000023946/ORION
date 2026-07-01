from src.infrastructure.real.http.http_client_port import HttpClientPort
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_port import ToolPort
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.web_search.web_search_request import WebSearchRequest
from src.infrastructure.real.mcp_server.tools.web_search.web_search_response import WebSearchResponse
from src.ports.tool_response import ToolResponse
from src.infrastructure.config.settings import settings


class WebSearchTool(ToolPort):

    def __init__(self, http_client: HttpClientPort):
        self.http_client = http_client

    async def execute(self, tool_request: ToolRequest) -> ToolResponse:

        # ----------------------------
        # 1. Build typed request
        # ----------------------------
        request = WebSearchRequest.create(tool_request)

        # ----------------------------
        # 2. Call external API
        # ----------------------------
        raw_response = await self.http_client.post(
            url=settings.web_api,
            json={
                "query": request.query
            }
        )

        # ----------------------------
        # 3. Convert raw API → domain object
        # ----------------------------
        web_search_response = WebSearchResponse.create(raw_response)

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