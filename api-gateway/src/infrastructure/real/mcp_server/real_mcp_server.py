
from src.domain.tool import Tool
from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_information_registry import ToolInformationRegistry
from src.infrastructure.real.mcp_server.tools.core.tool_registry_port import ToolRegistryPort
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.ports.mcp_server_port import MCPServerPort
from src.ports.tool_response import ToolResponse

class RealMCPServer(MCPServerPort):
    def __init__(
        self, 
        tool_registry_port: ToolRegistryPort, 
        tool_information_registry: ToolInformationRegistry
    ):
        self.tool_registry_port = tool_registry_port
        self.tool_information_registry = tool_information_registry

    async def get_tools(self) -> list[Tool]:
        return self.tool_information_registry.get_all_information()

    async def call_tool(self, tool_name: ToolName, tool_request: ToolRequest) -> ToolResponse:
        return await self.tool_registry_port.call_tool(tool_name, tool_request)