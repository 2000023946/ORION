
from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_io_keys import ToolIOKeys
from src.infrastructure.real.mcp_server.tools.core.tool_output_registry import ToolOutputRegistry
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.core.tool_request_factory import ToolRequestFactory


class DocsIdsRequestFactory(ToolRequestFactory):    
    def create(self, tool_name: ToolName, tool_output_registry: ToolOutputRegistry) -> ToolRequest:
        docs_ids = tool_output_registry.get(ToolIOKeys.DOCS_IDS)
        tool_request = ToolRequest(
            tool_name=tool_name, 
            params={
                ToolIOKeys.DOCS_IDS: docs_ids
            }
        )
        return tool_request
    
