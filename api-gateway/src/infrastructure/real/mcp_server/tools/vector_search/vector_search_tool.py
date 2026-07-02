from src.infrastructure.config.settings import settings
from src.infrastructure.real.mcp_server.tools.core.tool_port import ToolPort
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.vector_search.embedding_port import EmbeddingPort
from src.infrastructure.real.mcp_server.tools.vector_search.vector_search_request import VectorSearchRequest
from src.infrastructure.real.mcp_server.tools.vector_search.vector_search_result import VectorSearchResult
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.vector_search.vector_store_port import VectorStorePort
from src.ports.tool_response import ToolResponse


class VectorSearchTool(ToolPort):

    def __init__(self, vector_store: VectorStorePort, embedder: EmbeddingPort):
        self.vector_store = vector_store
        self.embedder = embedder

    async def execute(self, tool_request: ToolRequest) -> ToolResponse:

        # ----------------------------
        # 1. Parse request
        # ----------------------------
        request = VectorSearchRequest.create(tool_request)
        query_text = request.query

        # ----------------------------
        # 2. Embed query → vector
        # ----------------------------
        query_vector = self.embedder.embed(query_text.text)

        # ----------------------------
        # 3. Vector search (FAISS / Pinecone / API)
        # ----------------------------
        search_response = self.vector_store.search(query_vector, settings.vector_top_k)


        # ----------------------------
        # 4. Convert raw → domain objects
        # ----------------------------
        results = VectorSearchResult.from_raw_list(search_response)

        # ----------------------------
        # 5. Return ToolResponse (DAG layer)
        # ----------------------------
        return ToolResponse(
            tool_name=request.tool_name,
            output={
                ToolIOKeys.DOCS_IDS: [
                    {
                        "id": r.doc_id.doc_id,
                        "score": r.score
                    }
                    for r in results
                ]
            },
            success=True
        )