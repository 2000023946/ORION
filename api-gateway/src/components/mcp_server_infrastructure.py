from src.components.tools_infrastructure.db_filter_infrastructure import DBFilterInfrastructure
from src.components.tools_infrastructure.metadata_filter_infrastructure import MetadataFilterInfrastructure
from src.components.tools_infrastructure.vector_search_infrastructure import VectorSearchInfrasture
from src.components.tools_infrastructure.web_search_infrastructure import WebSearchInfrastructure
from src.infrastructure.real.mcp_server.real_mcp_server import RealMCPServer
from src.infrastructure.real.mcp_server.tools.core.tool_information import DB_FILTER_TOOL, METADATA_FILTER_TOOL, VECTOR_SEARCH_TOOL, WEB_SEARCH_TOOL
from src.infrastructure.real.mcp_server.tools.core.tool_information_registry import ToolInformationRegistry
from src.infrastructure.real.mcp_server.tools.core.tool_registry_port import ToolRegistryPort

class MCPServerInfrastructure:
    def __init__(self, mock: bool = False):
        # Register tool metadata
        tool_information_registry = ToolInformationRegistry()
        tool_information_registry.register(VECTOR_SEARCH_TOOL.name, VECTOR_SEARCH_TOOL)
        tool_information_registry.register(WEB_SEARCH_TOOL.name, WEB_SEARCH_TOOL)
        tool_information_registry.register(METADATA_FILTER_TOOL.name, METADATA_FILTER_TOOL)
        tool_information_registry.register(DB_FILTER_TOOL.name, DB_FILTER_TOOL)

        # Keep infrastructure objects
        self.vector_search_infra = VectorSearchInfrasture()
        self.web_search_infra = WebSearchInfrastructure()
        self.metadata_filter_infra = MetadataFilterInfrastructure()
        self.db_filter_infra = DBFilterInfrastructure()

        # Build tools
        vector_tool = self.vector_search_infra.build()
        web_tool = self.web_search_infra.build()
        metadata_tool = self.metadata_filter_infra.build()
        db_tool = self.db_filter_infra.build()

        tool_registry = ToolRegistryPort()
        tool_registry.register(VECTOR_SEARCH_TOOL.name, vector_tool)
        tool_registry.register(WEB_SEARCH_TOOL.name, web_tool)
        tool_registry.register(METADATA_FILTER_TOOL.name, metadata_tool)
        tool_registry.register(DB_FILTER_TOOL.name, db_tool)

        self.mcp_server = RealMCPServer(
            tool_registry_port=tool_registry,
            tool_information_registry=tool_information_registry,
        )
        
        if mock:
            self.use_mock()
        else:
            self.use_real()
        
    def use_mock(self):
        self.web_search_infra.use_mock()
        self.db_filter_infra.use_mock()

    def use_real(self):
        self.web_search_infra.use_real()
        self.db_filter_infra.use_real()