from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Document:
    doc_id: str
    title: str
    content: str
    price: str
    metadata: dict[str, Any]

    @classmethod
    def from_raw(cls, raw: dict[str, Any]) -> "Document":
        obj =  cls(
            doc_id=raw["_id"],
            title=raw.get("title", ""),
            content=raw.get("content", ""),
            price=raw.get('price', ''),
            metadata=raw.get("metadata", {})
        )
        return obj

    @classmethod
    def from_raw_list(cls, raw_list: list[dict[str, Any]]) -> list["Document"]:
        return [cls.from_raw(item) for item in raw_list]