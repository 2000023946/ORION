from dataclasses import dataclass

from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.vector_search.doc_id import DocId

@dataclass
class MetadataFilterRequest(ToolRequest):
    docs_ids: list[DocId]
    @classmethod
    def create(cls, tool_request: ToolRequest) -> MetadataFilterRequest:
        if ToolIOKeys.DOCS_IDS not in tool_request.params:
            raise ValueError("Web search cannot be called without query param")
        
        docs_ids = tool_request.params[ToolIOKeys.QUERY]

        return MetadataFilterRequest(
            tool_name=tool_request.tool_name, 
            docs_ids=docs_ids,
            params=tool_request.params
        )