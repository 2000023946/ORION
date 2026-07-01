from typing import Any

from src.domain.query import Query
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.ports.tool_response import ToolResponse


class ToolOutputRegistry:
    def __init__(self, query: Query):
        self.registry: dict[ToolIOKeys, Any] = {}
        self.registry[ToolIOKeys.QUERY] = query
    
    def save_response(self, response: ToolResponse):
        for key, value in response.output.items():
            self.registry[key] = value
    
    def get(self, key: ToolIOKeys) -> Any:
        if key not in self.registry:
            raise ValueError(f"Accessing key: {key} not in ToolOutputRegistry")
        return self.registry[key]