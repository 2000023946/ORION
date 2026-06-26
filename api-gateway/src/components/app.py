from src.application.mcp_orchestrator import MCPOrchestrator

from src.infrastructure.real.http.requests_http_adapter import RequestsHTTPAdapter

from src.infrastructure.real.tools.vector_service.vector_search_tool import VectorSearchTool
from src.infrastructure.real.tools.filter_service.filter_tool import FilterTool
from src.infrastructure.real.tools.metadata_service.metadata_tool import MetadataTool
from src.infrastructure.real.tools.web_search_adapter.web_search_tool import WebSearchTool


class Application:
    def __init__(self):
        http = RequestsHTTPAdapter()

        self.vector_tool = VectorSearchTool(http)
        self.filter_tool = FilterTool(http)
        self.metadata_tool = MetadataTool(http)
        self.web_tool = WebSearchTool(http)

        self.orchestrator = MCPOrchestrator(
            vector_tool=self.vector_tool,
            filter_tool=self.filter_tool,
            metadata_tool=self.metadata_tool,
            web_tool=self.web_tool,
        )


app = Application()