from abc import ABC, abstractmethod
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.ports.tool_response import ToolResponse
class ToolPort(ABC):
    @abstractmethod
    def execute(self, tool_request: ToolRequest) -> ToolResponse:
        pass