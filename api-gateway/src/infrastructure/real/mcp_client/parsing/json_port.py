from abc import ABC, abstractmethod
from typing import Any, Dict

class JsonPort(ABC):

    @abstractmethod
    def to_json(self, data: str) -> Dict[str, Any]:
        """Convert object to JSON-serializable dictionary."""
        pass
