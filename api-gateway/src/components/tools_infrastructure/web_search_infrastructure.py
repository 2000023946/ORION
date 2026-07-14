from src.infrastructure.real.mcp_server.tools.web_search.http_web_search_client import HttpWebSearchClient
from src.infrastructure.real.mcp_server.tools.web_search.mock_web_search_client import MockWebSearchClient
from src.infrastructure.real.mcp_server.tools.web_search.web_search_tool import WebSearchTool


class WebSearchInfrastructure:
    def __init__(self):
        self.tool = None

    def build(self) -> WebSearchTool:
        from src.infrastructure.real.http.real_http_client import RealHttpClient
        from src.infrastructure.real.mcp_server.tools.web_search.web_search_tool import WebSearchTool

        http_client = RealHttpClient()
        self.fake_web_search_client = MockWebSearchClient()
        self.search_client = HttpWebSearchClient(http_client)
        self.tool = WebSearchTool(self.search_client)

        return self.tool
    
    def use_mock(self):
        if not self.tool:
            raise ValueError("must build first")
        self.tool.web_search_client = self.fake_web_search_client
        
    def use_real(self):
        if not self.tool:
            raise ValueError("must build first")
        self.tool.web_search_client = self.search_client
    