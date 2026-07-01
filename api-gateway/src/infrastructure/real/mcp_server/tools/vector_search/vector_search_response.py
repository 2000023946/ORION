from dataclasses import dataclass
from typing import Optional, Any

from src.infrastructure.real.mcp_server.tools.vector_search.vector_search_result import VectorSearchResult


@dataclass
class VectorSearchResponse:
    query: str
    results: list[VectorSearchResult]
    metadata: Optional[dict[str, Any]] = None