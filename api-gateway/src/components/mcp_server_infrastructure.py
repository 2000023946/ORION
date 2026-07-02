from src.domain.input import Input
from src.domain.output import Output
from src.domain.tool import Tool
from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.real_mcp_server import RealMCPServer
from src.infrastructure.real.mcp_server.tools.core.tool_information_registry import ToolInformationRegistry
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_registry_port import ToolRegistryPort


class MCPServerInfrastructure:
    def __init__(self):
        # Make the tool Names
        VECTOR_SEARCH_TOOL = ToolName("VECTOR_SEARCH_TOOL")

        # Fill in the registry information
        tool_information_registry = ToolInformationRegistry()
        tool_information_registry.register()
        tool_registry_port = ToolRegistryPort()
        self.mcp_server = RealMCPServer(
            tool_registry_port=tool_registry_port,
            tool_information_registry=tool_information_registry
        )