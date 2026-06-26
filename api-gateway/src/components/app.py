from src.application.mcp_orchestrator import MCPOrchestrator
from src.config import config
from src.infrastructure.dummy.dummy_http_port import DummyHttpAdapter

from src.infrastructure.real.tools.vector_service.vector_search_tool import VectorSearchTool
from src.infrastructure.real.tools.filter_service.filter_tool import FilterTool
from src.infrastructure.real.tools.metadata_service.metadata_tool import MetadataTool
from src.infrastructure.real.tools.web_search_adapter.web_search_tool import WebSearchTool


class Application:
    def __init__(self):
        http = DummyHttpAdapter()

        self.vector_tool = VectorSearchTool(http, config)
        self.filter_tool = FilterTool(http, config)
        self.metadata_tool = MetadataTool(http, config)
        self.web_tool = WebSearchTool(http, config)

        self.orchestrator = MCPOrchestrator(
            vector_tool=self.vector_tool,
            filter_tool=self.filter_tool,
            metadata_tool=self.metadata_tool,
            web_tool=self.web_tool,
        )


app = Application()