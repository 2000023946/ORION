from dataclasses import dataclass
from typing import Any
from src.infrastructure.real.mcp_server.tools.vector_search.doc_id import DocId


@dataclass(frozen=True)
class VectorSearchResult:
    doc_id: DocId
    score: float

    @classmethod
    def from_raw(cls, raw: dict[str, Any]) -> "VectorSearchResult":
        print("raw info", raw)
        return cls(
            doc_id=DocId(raw["doc_id"]),
            score=float(raw["score"])
        )

    @classmethod
    def from_raw_list(cls, raw_list: list[dict[str, Any]]) -> list["VectorSearchResult"]:
        return [cls.from_raw(item) for item in raw_list]