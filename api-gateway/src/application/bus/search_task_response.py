

from dataclasses import dataclass
from typing import Any, Optional

from src.application.bus.request_id import RequestID
from src.domain.search_answer import SearchAnswer


@dataclass
class SearchTaskResponse:
    request_id: RequestID
    success: bool
    answer: Optional[SearchAnswer] = None
    error: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None
    
    def to_dict(self):
        return {
            "request_id": self.request_id.value,
            "success": self.success,
            "answer": '' if not self.answer else self.answer.answer,
            "error": self.error,
            "metadata":self.metadata
        }
