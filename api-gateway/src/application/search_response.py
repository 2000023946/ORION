from dataclasses import dataclass
from typing import Any, Optional
from src.domain.search_answer import SearchAnswer


@dataclass
class SearchResponse:
    success: bool
    answer: Optional[SearchAnswer] = None
    metadata: Optional[dict[str, Any]] = None
    error: Optional[str] = None