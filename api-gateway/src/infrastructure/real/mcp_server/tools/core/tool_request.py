from dataclasses import dataclass
from typing import Any

from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys


@dataclass
class ToolRequest:
    tool_name: ToolName
    params: dict[ToolIOKeys, Any]
    
    def get(self, tool_input: ToolIOKeys):
        if tool_input not in self.params:
            raise ValueError(f"Tool Input {tool_input} not in Tool request")

        return self.params[tool_input]

