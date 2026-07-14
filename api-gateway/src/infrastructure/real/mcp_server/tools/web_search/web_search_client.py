from abc import ABC, abstractmethod

from src.domain.query import Query
from src.infrastructure.real.mcp_server.tools.web_search.web_search_response import WebSearchResponse


class WebSearchClient(ABC):
    @abstractmethod
    async def search(self, query: Query, retry_limit: int=5) -> WebSearchResponse:
        pass