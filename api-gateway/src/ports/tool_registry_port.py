from abc import ABC, abstractmethod
from typing import List
from src.ports.tool_execution_port import ToolExecutionPort

class ToolRegistryPort(ABC):

    @abstractmethod
    def get_tools(self) -> List[ToolExecutionPort]:
        pass