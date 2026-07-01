from dataclasses import dataclass
from typing import Any

from src.infrastructure.real.mcp_server.tools.vector_search.vector_search_result import VectorSearchResult


@dataclass
class VectorSearchResponse:
    query: str
    results: list[VectorSearchResult]

    @classmethod
    def from_api(cls, query: str, raw: dict[str, Any]) -> "VectorSearchResponse":
        return cls(
            query=query,
            results=VectorSearchResult.from_raw_list(raw["matches"])
        )