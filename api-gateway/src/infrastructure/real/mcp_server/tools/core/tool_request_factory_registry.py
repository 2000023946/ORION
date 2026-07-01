from src.domain.tool_name import ToolName
from src.infrastructure.real.mcp_server.tools.core.tool_output_registry import ToolOutputRegistry
from src.infrastructure.real.mcp_server.tools.core.tool_request import ToolRequest
from src.infrastructure.real.mcp_server.tools.core.tool_request_factory import ToolRequestFactory


class ToolRequestFactoryRegistry:
    def __init__(self):
        self.registry: dict[ToolName, ToolRequestFactory] = {}
    
    def register_factory(self, tool_name: ToolName, tool_request_factory: ToolRequestFactory):
        self.registry[tool_name] = tool_request_factory
    
    def create_request(self, tool_name: ToolName, tool_output_registry: ToolOutputRegistry) -> ToolRequest:
        if tool_name not in self.registry:
            raise ValueError(f"cannot create tool {tool_name} not registered in tool request factory")
        
        factory: ToolRequestFactory = self.registry[tool_name]
        request: ToolRequest = factory.create(tool_name, tool_output_registry)
        
        return request
