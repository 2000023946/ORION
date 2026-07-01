from typing import List

from src.ports.tool_registry_port import ToolRegistryPort
from src.ports.tool_execution_port import ToolExecutionPort
from src.domain.tool_type import ToolType

from src.config import Config
from src.ports.http_port import HttpPort

from src.infrastructure.real.tools.vector_service.vector_search_tool import VectorSearchTool
from src.infrastructure.real.tools.filter_service.filter_tool import FilterTool
from src.infrastructure.real.tools.metadata_service.metadata_tool import MetadataTool
from src.infrastructure.real.tools.web_search_adapter.web_search_tool import WebSearchTool


class ToolRegistry(ToolRegistryPort):

    def __init__(self, http_adapter: HttpPort, config: Config):
        self.http_adapter = http_adapter
        self.config = config

        # -------------------------
        # Instantiate tools once
        # -------------------------
        self._tools_map = {
            ToolType.VECTOR_SEARCH: VectorSearchTool(self.http_adapter, self.config),
            ToolType.FILTER: FilterTool(self.http_adapter, self.config),
            ToolType.METADATA: MetadataTool(self.http_adapter, self.config),
            ToolType.WEB_SEARCH: WebSearchTool(self.http_adapter, self.config),
        }

    # -------------------------
    # Return all tools (for LLM planning)
    # -------------------------
    def get_tools(self) -> List[ToolExecutionPort]:
        return list(self._tools_map.values())

    # -------------------------
    # Return single tool (for execution engine)
    # -------------------------
    def get_tool(self, tool_type: ToolType) -> ToolExecutionPort:
        if tool_type not in self._tools_map:
            raise ValueError(f"Unknown tool type: {tool_type}")

        return self._tools_map[tool_type]