import enum
from typing import Any

from src.domain.tool_name import ToolName

class Context:
    def __init__(self, context: dict[ToolName, Any] | None = None):
        self.context = context or {}

    def get(self, key: ToolName) -> Any:
        if key not in self.context:
            raise ValueError(f"Cannot get {key} from context")
        return self.context.get(key)
    
    def update(self, key: ToolName, value: Any):
        self.context[key] = value

    def __str__(self) -> str:
        if not self.context:
            return "Context(empty)"

        lines: list[str] = []
        for key, value in self.context.items():
            lines.append(f"{key}: {value}")

        return "\n".join(lines)
    
    def to_dict(self) -> dict[str, Any]:
        """
        Serializes the entire context into a pure, JSON-safe dictionary.
        Converts ToolName keys to strings and scrubs all nested objects.
        """
        json_doc =  self._make_json_safe(self.context)
        return json_doc

    def _make_json_safe(self, obj: Any) -> Any:
        """Recursively destroys Enums and custom classes for JSON dumping."""
        if isinstance(obj, dict):
            safe_dict = {}
            for k, v in obj.items():
                # Extract string from ToolName, Enum, or cast to string
                if isinstance(k, ToolName):
                    safe_key = k.name
                elif isinstance(k, enum.Enum):
                    safe_key = k.value
                else:
                    safe_key = str(k)
                safe_dict[safe_key] = self._make_json_safe(v)
            return safe_dict
            
        elif isinstance(obj, list):
            return [self._make_json_safe(item) for item in obj]
            
        elif hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
            return self._make_json_safe(obj.to_dict())
            
        elif hasattr(obj, '__dict__'):
            return self._make_json_safe(obj.__dict__)
            
        elif isinstance(obj, enum.Enum):
            return obj.value
            
        return obj

    def __str__(self) -> str:
        if not self.context:
            return "Context(empty)"
        lines: list[str] = []
        for key, value in self.context.items():
            lines.append(f"{key}: {value}")
        return "\n".join(lines)