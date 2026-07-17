import json
from dataclasses import dataclass, asdict
from typing import Any, Optional
from src.domain.search_answer import SearchAnswer


@dataclass
class SearchResponse:
    success: bool
    answer: Optional[SearchAnswer] = None
    metadata: Optional[dict[str, Any]] = None
    error: Optional[str] = None

    def to_json(self) -> str:
        """
        Serializes the dataclass instance to a JSON string.
        Using `asdict` automatically handles nested dataclasses (like SearchAnswer).
        """
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, json_str: str) -> "SearchResponse":
        """
        Deserializes a JSON string back into a structured SearchResponse instance,
        safely reconstructing nested dataclasses.
        """
        data = json.loads(json_str)
        
        # Reconstruct the nested SearchAnswer dataclass if it exists in the data
        answer_data = data.get("answer")
        if answer_data is not None and isinstance(answer_data, dict):
            data["answer"] = SearchAnswer(**answer_data)
            
        return cls(**data)