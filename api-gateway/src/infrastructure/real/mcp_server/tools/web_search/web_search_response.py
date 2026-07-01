from dataclasses import dataclass
from typing import Optional

from src.infrastructure.real.http.http_response import HttpResponse
from src.infrastructure.real.mcp_server.tools.web_search.web_search_result import WebSearchResult


@dataclass
class WebSearchResponse:
    query: str
    results: list[WebSearchResult]
    answer: Optional[str] = None

    @classmethod
    def create(cls, response: HttpResponse) -> "WebSearchResponse":
        """
        Convert raw web API JSON → structured domain object
        """

        results_raw = response.get("results", [])

        results: list[WebSearchResult] = [
            WebSearchResult(
                title=r.get("title", ""),
                url=r.get("url", ""),
                snippet=r.get("content", r.get("snippet", "")),
                score=r.get('score', None)
            )
            for r in results_raw
        ]

        return cls(
            query=response.get("query", ""),
            results=results,
            answer=response.get("answer"),
        )