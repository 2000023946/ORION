from dataclasses import dataclass
from typing import Optional, Any
from src.domain.tool_name import ToolName

@dataclass
class ToolResponse:
    tool_name: ToolName
    output: dict[str, Any]
    success: bool = True
    error: Optional[str] = None
    