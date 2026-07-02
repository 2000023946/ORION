from typing import Any, Dict
import json
from src.infrastructure.real.mcp_client.parsing.json_port import JsonPort


class JsonAdapter(JsonPort):
    
    def to_json(self, data: str) -> Dict[str, Any]:
        """Convert object to JSON-serializable dictionary."""
        return json.loads(data)
    