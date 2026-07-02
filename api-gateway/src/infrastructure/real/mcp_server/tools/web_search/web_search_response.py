from dataclasses import dataclass
from typing import Any, Optional
import json

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
        Convert raw web API JSON → structured domain object.
        """
        
        raw = response.body
        
        if isinstance(raw, str):
            data: dict[str, Any] = json.loads(raw)
        else:
            data: dict[str, Any] = raw or {}


        results = [
            WebSearchResult(
                title=r.get("title", ""),
                url=r.get("url", ""),
                snippet=r.get("content", r.get("snippet", "")),
                score=r.get("score"),
            )
            for r in data.get("results", [])
        ]

        return cls(
            query=data.get("query", ""),
            results=results,
            answer=data.get("answer"),
        )