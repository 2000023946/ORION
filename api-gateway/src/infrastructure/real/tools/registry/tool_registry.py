# src/infrastructure/real/tool_registry/tool_registry.py

from typing import List

from src.ports.tool_registry_port import ToolRegistryPort
from src.ports.tool_execution_port import ToolExecutionPort
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

    def get_tools(self) -> List[ToolExecutionPort]:
        return [
            VectorSearchTool(self.http_adapter, self.config),
            FilterTool(self.http_adapter, self.config),
            MetadataTool(self.http_adapter, self.config),
            WebSearchTool(self.http_adapter, self.config),
        ]