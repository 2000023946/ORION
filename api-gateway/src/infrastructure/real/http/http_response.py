from dataclasses import dataclass
from typing import Any


@dataclass
class HttpResponse:
    status_code: int
    headers: dict[str, Any]
    body: Any

    def get(self, key: str, default: Any = None) -> Any:
        return self.body.get(key, default)

    def require(self, key: str) -> Any:
        print(self.body)
        if key not in self.body:
            print("missing key", key)
            raise KeyError(f"Missing required key: {key}")
        return self.body[key]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status_code": self.status_code,
            "headers": self.headers,
            "body": self.body,
        }