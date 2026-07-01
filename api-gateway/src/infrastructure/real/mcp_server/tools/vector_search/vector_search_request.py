from dataclasses import dataclass

from src.domain.query import Query
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest

@dataclass
class VectorSearchRequest(ToolRequest):
    query: Query
    @classmethod
    def create(cls, tool_request: ToolRequest) -> VectorSearchRequest:
        if ToolIOKeys.QUERY not in tool_request.params:
            raise ValueError("Web search cannot be called without query param")
        
        query = tool_request.params[ToolIOKeys.QUERY]

        return VectorSearchRequest(
            tool_name=tool_request.tool_name, 
            query=query,
            params=tool_request.params
        )