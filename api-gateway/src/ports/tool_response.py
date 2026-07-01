from dataclasses import dataclass
from typing import Optional, Any
from src.domain.tool_name import ToolName
from src.infrastructure.real.graph_executor.real_graph_executor import ToolInputs

@dataclass
class ToolResponse:
    tool_name: ToolName
    output: dict[ToolInputs, Any]
    success: bool = True
    error: Optional[str] = None
    