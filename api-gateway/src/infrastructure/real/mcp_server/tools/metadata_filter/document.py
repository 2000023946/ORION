from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Document:
    doc_id: str
    title: str
    content: str
    metadata: dict[str, Any]

    @classmethod
    def from_raw(cls, raw: dict[str, Any]) -> "Document":
        return cls(
            doc_id=raw["id"],
            title=raw.get("title", ""),
            content=raw.get("content", ""),
            metadata=raw.get("metadata", {})
        )

    @classmethod
    def from_raw_list(cls, raw_list: list[dict[str, Any]]) -> list["Document"]:
        return [cls.from_raw(item) for item in raw_list]