from dataclasses import dataclass


@dataclass(frozen=True)
class VectorSearchResult:
    doc_id: str
    score: float