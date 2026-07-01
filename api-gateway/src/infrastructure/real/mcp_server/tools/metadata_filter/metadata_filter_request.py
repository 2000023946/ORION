from dataclasses import dataclass

from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.vector_search.doc_id import DocId


@dataclass
class MetadataFilterRequest(ToolRequest):
    docs_ids: list[DocId]

    @classmethod
    def create(cls, tool_request: ToolRequest) -> "MetadataFilterRequest":
        """
        Converts generic ToolRequest → MetadataFilterRequest
        """

        if ToolIOKeys.DOCS_IDS not in tool_request.params:
            raise ValueError("Metadata filter requires DOCS_IDS param")

        docs_ids = tool_request.params[ToolIOKeys.DOCS_IDS]

        return cls(
            tool_name=tool_request.tool_name,
            docs_ids=docs_ids,
            params=tool_request.params,
        )

    def serialize_ids(self) -> list[str]:
        """
        Converts request → JSON-ready dict for HTTP / DB layer
        """

        return [doc_id.doc_id for doc_id in self.docs_ids]