from src.infrastructure.real.mcp_server.tools.web_search.http_web_search_client import HttpWebSearchClient
from src.infrastructure.real.mcp_server.tools.web_search.web_search_tool import WebSearchTool


class WebSearchInfrastructure:
    def __init__(self):
        self.tool = None

    def build(self) -> WebSearchTool:
        from src.infrastructure.real.http.real_http_client import RealHttpClient
        from src.infrastructure.real.mcp_server.tools.web_search.web_search_tool import WebSearchTool

        http_client = RealHttpClient()
        search_client = HttpWebSearchClient(http_client)
        self.tool = WebSearchTool(search_client)

        return self.tool