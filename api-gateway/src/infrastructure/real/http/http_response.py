from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class HttpResponse:
    status_code: int
    headers: Dict[str, Any]
    body: Any

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)

    def require(self, key: str) -> Any:
        if not hasattr(self, key):
            raise KeyError(f"Missing required key: {key}")
        return getattr(self, key)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status_code": self.status_code,
            "headers": self.headers,
            "body": self.body,
        }