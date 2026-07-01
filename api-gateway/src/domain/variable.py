from dataclasses import dataclass

from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys


@dataclass
class Variable:
    name: ToolIOKeys
    type: str
    description: str
    required: bool = True