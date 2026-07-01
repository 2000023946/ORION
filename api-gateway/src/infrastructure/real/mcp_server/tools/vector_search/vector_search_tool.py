
from src.infrastructure.config.settings import settings
from src.infrastructure.real.http.http_client_port import HttpClientPort
from src.infrastructure.real.mcp_server.tools.core.tool_port import ToolPort
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.vector_search.vector_search_request import VectorSearchRequest
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.ports.tool_response import ToolResponse


class VectorSearchTool(ToolPort):

    def __init__(self, http_client: HttpClientPort):
        self.http_client = http_client

    async def execute(self, tool_request: ToolRequest) -> ToolResponse:

        # ----------------------------
        # 1. Build typed request
        # ----------------------------
        request = VectorSearchRequest.create(tool_request)

        query_text = request.query

        # ----------------------------
        # 2. Embed query
        # ----------------------------
        embedding_response = await self.http_client.post(
            url=f"{settings.embedding_api}/embed",
            json={
                "model": settings.embedding_model,
                "input": query_text
            },
            timeout=settings.http_timeout
        )

        query_vector = embedding_response.require("embedding")

        # ----------------------------
        # 3. Vector search (FAISS / Pinecone / API)
        # ----------------------------
        search_response = await self.http_client.post(
            url=f"{settings.vector_db_url}/search",
            json={
                "index": settings.vector_db_index,
                "vector": query_vector,
                "top_k": settings.vector_top_k
            },
            timeout=settings.http_timeout
        )

        # ----------------------------
        # 4. Extract results
        # ----------------------------
        matches = search_response.require("matches")

        results = [
            {
                "id": m["id"],
                "score": m["score"]
            }
            for m in matches
        ]

        # ----------------------------
        # 5. Return ToolResponse
        # ----------------------------
        return ToolResponse(
            tool_name=request.tool_name,
            output={
                ToolIOKeys.DOC_IDS: results
            },
            success=True
        )