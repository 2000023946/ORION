from abc import  abstractmethod


from src.domain.tool import Tool
from src.domain.tool_name import ToolName
from src.ports.mcp_server_port import MCPServerPort
from src.ports.tool_response import ToolResponse


class RealMCPServer(MCPServerPort):

    async def get_tools(self) -> list[Tool]:
        return [
        ]

    @abstractmethod
    async def call_tool(self, tool_name: ToolName) -> ToolResponse:
        return pass