from abc import ABC, abstractmethod

from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_output_registry import ToolOutputRegistry
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest


class ToolRequestFactory(ABC):    
    @abstractmethod
    def create(self, tool_name: ToolName, tool_output_registry: ToolOutputRegistry) -> ToolRequest:
        pass
