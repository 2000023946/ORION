from dataclasses import dataclass
from typing import Any

from src.infrastructure.real.mcp_server.tools.metadata_filter.document import Document


@dataclass
class DBFilterResponse:
    documents: list[Document]

    @classmethod
    def from_raw(cls, raw: list[dict[str, Any]]) -> "DBFilterResponse":
        return cls(
            documents=Document.from_raw_list(raw)
        )