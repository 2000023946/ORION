from abc import  abstractmethod


from src.constants.constants import START_TOOL
from src.domain.tool import Tool
from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.ports.mcp_server_port import MCPServerPort
from src.ports.tool_response import ToolResponse


class RealMCPServer(MCPServerPort):

    async def get_tools(self) -> list[Tool]:
        return [
        ]

    @abstractmethod
    async def call_tool(self, tool_name: ToolName, tool_request: ToolRequest) -> ToolResponse:
        return ToolResponse(tool_name=START_TOOL, output={ToolIOKeys.QUERY: 'a'})