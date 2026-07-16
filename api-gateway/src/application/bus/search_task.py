from dataclasses import dataclass

from src.application.bus.request_id import RequestID
from src.domain.query import Query

@dataclass
class SearchTask:
    request_id: RequestID
    query: Query