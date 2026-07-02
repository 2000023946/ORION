
from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_output_registry import ToolOutputRegistry
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.core.tool_request_factory import ToolRequestFactory


class QueryRequestFactory(ToolRequestFactory):    
    def create(self, tool_name: ToolName, tool_output_registry: ToolOutputRegistry) -> ToolRequest:
        query = tool_output_registry.get(ToolIOKeys.QUERY)
        tool_request = ToolRequest(
            tool_name=tool_name, 
            params={
                ToolIOKeys.QUERY: query
            }
        )
        return tool_request
    
