from abc import ABC, abstractmethod
from src.domain.tool import Tool
from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.ports.tool_response import ToolResponse

class MCPServerPort(ABC):
    
    @abstractmethod
    async def get_tools(self) -> list[Tool]:
        pass
    
    @abstractmethod
    async def call_tool(self, tool_name: ToolName, tool_request: ToolRequest) -> ToolResponse:
        pass
    