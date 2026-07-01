from dataclasses import dataclass
from typing import Any


@dataclass
class HttpResponse:
    _data: dict[str, Any]

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def require(self, key: str) -> Any:
        if key not in self._data:
            raise KeyError(f"Missing required key: {key}")
        return self._data[key]

    def to_dict(self) -> dict[str, Any]:
        return self._data