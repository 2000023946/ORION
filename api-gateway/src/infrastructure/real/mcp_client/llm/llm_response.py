from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMResponse:
    """
    Simple wrapper for raw LLM output only.
    """
    raw: str
    error: Optional[str] = None

    def is_error(self) -> bool:
        return self.error is not None
    
    def get_response(self) -> str:
        if self.is_error():
            raise ValueError(f"Failed to create response. due to {self.error}")
        return self.raw