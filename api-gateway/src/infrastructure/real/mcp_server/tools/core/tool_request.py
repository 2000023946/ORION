from dataclasses import dataclass
from typing import Any

from src.infrastructure.real.mcp_server.tools.core.tool_inputs import ToolInputs


@dataclass
class ToolRequest:
    params: dict[ToolInputs, Any]

