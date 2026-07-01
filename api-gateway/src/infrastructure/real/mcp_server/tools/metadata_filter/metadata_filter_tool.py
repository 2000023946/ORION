from src.infrastructure.config.settings import settings
from src.infrastructure.real.http.http_client_port import HttpClientPort
from src.infrastructure.real.mcp_server.tools.core.tool_port import ToolPort
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys

from src.infrastructure.real.mcp_server.tools.metadata_filter.metadata_response import MetadataResponse
from src.ports.tool_response import ToolResponse


class MetadataFilterTool(ToolPort):

    def __init__(self, http_client: HttpClientPort):
        self.http_client = http_client

    async def execute(self, tool_request: ToolRequest) -> ToolResponse:

        # ----------------------------
        # 1. Extract input (doc ids from vector search)
        # ----------------------------
        doc_ids = tool_request.params.get(ToolIOKeys.DOC_IDS)

        if not doc_ids:
            return ToolResponse(
                tool_name=tool_request.tool_name,
                output={ToolIOKeys.DOCUMENTS: []},
                success=False,
                error="No document ids provided"
            )

        # extract only ids
        ids = [d["id"] for d in doc_ids]

        # ----------------------------
        # 2. Query metadata DB
        # ----------------------------
        response = await self.http_client.post(
            url=f"{settings.metadata_db_url}/query",
            json={
                "index": settings.metadata_db_index,
                "filter": {
                    "id": {"$in": ids}
                }
            },
            timeout=settings.http_timeout
        )

        # ----------------------------
        # 3. Parse response → domain objects
        # ----------------------------
        raw_docs = response.require("documents")

        metadata_response = MetadataResponse.from_raw(raw_docs)

        # ----------------------------
        # 4. Return ToolResponse
        # ----------------------------
        return ToolResponse(
            tool_name=tool_request.tool_name,
            output={
                ToolIOKeys.DOCUMENTS: [
                    {
                        "id": d.doc_id,
                        "title": d.title,
                        "content": d.content,
                        "metadata": d.metadata
                    }
                    for d in metadata_response.documents
                ]
            },
            success=True
        )