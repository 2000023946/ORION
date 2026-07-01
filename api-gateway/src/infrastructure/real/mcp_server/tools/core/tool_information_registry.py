from src.domain.tool import Tool
from src.domain.tool_name import ToolName


class ToolInformationRegistry:
    def __init__(self):
        self.registry: dict[ToolName, Tool] = {}
    
    def register(self, tool_name: ToolName, tool_information: Tool):
        self.registry[tool_name] = tool_information
    
    def get_information(self, tool_name: ToolName) -> Tool:
        return self.registry[tool_name]
    
    def get_all_information(self) -> list[Tool]:
        return [tool for tool in self.registry.values()]