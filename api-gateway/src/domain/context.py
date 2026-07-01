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