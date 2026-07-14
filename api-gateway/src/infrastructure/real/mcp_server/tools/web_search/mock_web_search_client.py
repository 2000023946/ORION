import asyncio

from src.domain.query import Query
from src.infrastructure.real.mcp_server.tools.web_search.web_search_client import WebSearchClient
from src.infrastructure.real.mcp_server.tools.web_search.web_search_response import WebSearchResponse
from src.infrastructure.real.mcp_server.tools.web_search.web_search_result import WebSearchResult


class MockWebSearchClient(WebSearchClient):

    async def search(self, query: Query, retry_limit: int = 5) -> WebSearchResponse:
            
        # simulate network latency
        await asyncio.sleep(1.4)

        return WebSearchResponse(
            query=query.text,
            results=[
                WebSearchResult(
                    title="U.S. Stock Markets Today",
                    url="https://www.example.com/markets",
                    snippet=(
                        "Quotes displayed in real-time or delayed. "
                        "Market data provided by simulated provider. "
                        "Technology sector +0.25%, Healthcare sector -0.79%, "
                        "Financial sector +0.31%."
                    ),
                    score=0.47957736
                ),

                WebSearchResult(
                    title="U.S. Stock Market Headlines | Breaking Stock Market News",
                    url="https://www.example.com/reuters-markets",
                    snippet=(
                        "Latest stock market updates and financial news. "
                        "S&P 500 index trading lower by simulated market data. "
                        "Dow Jones Industrial Average and Nasdaq updates available."
                    ),
                    score=0.34329836
                ),

                WebSearchResult(
                    title="Market Activity",
                    url="https://www.example.com/nasdaq",
                    snippet=(
                        "Market activity including stocks, ETFs, indexes, "
                        "mutual funds, cryptocurrency, and economic calendars."
                    ),
                    score=0.3271097
                ),

                WebSearchResult(
                    title="US Markets, World Markets, and Stock Quotes",
                    url="https://www.example.com/cnn-markets",
                    snippet=(
                        "Global market information including US stocks, "
                        "commodities, currencies, bonds, and market trends."
                    ),
                    score=0.24359787
                ),

                WebSearchResult(
                    title="US Markets News - CNBC",
                    url="https://www.example.com/cnbc-markets",
                    snippet=(
                        "Financial news, stock indexes, commodities, "
                        "treasury updates, currencies, and market data."
                    ),
                    score=0.18532747
                ),
            ],
            answer=None
        )