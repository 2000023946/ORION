from abc import ABC, abstractmethod
from src.domain.tool import Tool
from src.domain.tool_name import ToolName
from src.ports.tool_response import ToolResponse

class MCPServerPort(ABC):
    
    @abstractmethod
    async def get_tools(self) -> list[Tool]:
        pass
    
    @abstractmethod
    async def call_tool(self, tool_name: ToolName) -> ToolResponse:
        pass
    