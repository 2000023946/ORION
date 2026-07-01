from abc import ABC, abstractmethod
from typing import List
from src.ports.tool_execution_port import ToolExecutionPort
from src.domain.tool_type import ToolType

class ToolRegistryPort(ABC):

    @abstractmethod
    def get_tools(self) -> List[ToolExecutionPort]:
        pass
    
    @abstractmethod
    def get_tool(self, tool_type: ToolType) -> ToolExecutionPort:
        pass