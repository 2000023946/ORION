from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_port import ToolPort
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.ports.tool_response import ToolResponse


class ToolRegistryPort:
    def __init__(self):
        self.registry: dict[ToolName, ToolPort] = {}
    
        
    def register(self, tool_name: ToolName, tool_port: ToolPort):
        self.registry[tool_name] = tool_port
    
    async def call_tool(self, tool_name: ToolName, tool_request: ToolRequest) -> ToolResponse:
        tool: ToolPort = self.registry[tool_name]
        tool_response: ToolResponse = await tool.execute(tool_request)
        
        return tool_response