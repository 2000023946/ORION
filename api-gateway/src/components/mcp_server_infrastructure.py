from src.components.tools_infrastructure.db_filter_infrastructure import DBFilterInfrastructure
from src.components.tools_infrastructure.metadata_filter_infrastructure import MetadataFilterInfrastructure
from src.components.tools_infrastructure.vector_search_infrastructure import VectorSearchInfrasture
from src.components.tools_infrastructure.web_search_infrastructure import WebSearchInfrastructure
from src.infrastructure.real.mcp_server.real_mcp_server import RealMCPServer
from src.infrastructure.real.mcp_server.tools.core.tool_information import DB_FILTER_TOOL, METADATA_FILTER_TOOL, VECTOR_SEARCH_TOOL, WEB_SEARCH_TOOL
from src.infrastructure.real.mcp_server.tools.core.tool_information_registry import ToolInformationRegistry
from src.infrastructure.real.mcp_server.tools.core.tool_registry_port import ToolRegistryPort


class MCPServerInfrastructure:
    def __init__(self):
        # REGISTER THE TOOLS
        tool_information_registry = ToolInformationRegistry()
        tool_information_registry.register(VECTOR_SEARCH_TOOL.name, VECTOR_SEARCH_TOOL)
        tool_information_registry.register(WEB_SEARCH_TOOL.name, WEB_SEARCH_TOOL)
        tool_information_registry.register(METADATA_FILTER_TOOL.name, METADATA_FILTER_TOOL)
        tool_information_registry.register(DB_FILTER_TOOL.name, DB_FILTER_TOOL)
        
        # INITIALIZE TOOLS INFRAS
        vector_search_tool = VectorSearchInfrasture().build()
        web_search_tool = WebSearchInfrastructure().build()
        metadata_filter_tool = MetadataFilterInfrastructure().build()
        db_filter_tool = DBFilterInfrastructure().build()
        
        # REGISTER THE TOOL PORTS
        tool_registry_port = ToolRegistryPort()
        tool_registry_port.register(VECTOR_SEARCH_TOOL.name, vector_search_tool)
        tool_registry_port.register(WEB_SEARCH_TOOL.name, web_search_tool)
        tool_registry_port.register(METADATA_FILTER_TOOL.name, metadata_filter_tool)
        tool_registry_port.register(DB_FILTER_TOOL.name, db_filter_tool)
        
        # CREATE THE MCP SERVER
        self.mcp_server = RealMCPServer(
            tool_registry_port=tool_registry_port,
            tool_information_registry=tool_information_registry
        )