from src.domain.query import Query
from src.infrastructure.config.settings import settings
from src.infrastructure.real.http.http_client_port import HttpClientPort
from src.infrastructure.real.mcp_server.tools.web_search.web_search_client import WebSearchClient
from src.infrastructure.real.mcp_server.tools.web_search.web_search_response import WebSearchResponse


class HttpWebSearchClient(WebSearchClient):
    def __init__(self, http_client: HttpClientPort):
        self.http_client = http_client
        
    
    async def search(self, query: Query, retry_limit: int = 5) -> WebSearchResponse:
        raw_response = await self.http_client.post(
            url=settings.web_api_url,
            json={
                "api_key": settings.web_api_key,
                "query": query.text,
                "max_results": retry_limit
            }
        )
        

        # ----------------------------
        # 3. Convert raw API → domain object
        # ----------------------------
        web_search_response = WebSearchResponse.create(raw_response)
        
        return web_search_response
    