from dataclasses import dataclass
from typing import Optional, Any
from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys

@dataclass
class ToolResponse:
    tool_name: ToolName
    output: dict[ToolIOKeys, Any]
    success: bool = True
    error: Optional[str] = None
    