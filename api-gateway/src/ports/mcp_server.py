from abc import ABC, abstractmethod
from src.domain.tool import Tool
from src.domain.tool_name import ToolName
from src.domain.tool_response import ToolResponse

class MCPServer(ABC):
    
    @abstractmethod
    def get_tools(self) -> list[Tool]:
        pass
    
    @abstractmethod
    def call_tool(self, tool_name: ToolName) -> ToolResponse:
        pass
    