from dataclasses import dataclass
from typing import Optional
from src.domain.search_answer import SearchAnswer


@dataclass
class SearchResponse:
    success: bool
    answer: Optional[SearchAnswer] = None
    error: Optional[str] = None