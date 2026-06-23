from abc import ABC, abstractmethod


class ToolRegistryPort(ABC):

    @abstractmethod
    def get_tools(self) -> list:
        pass