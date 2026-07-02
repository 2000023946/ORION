from abc import ABC, abstractmethod
from typing import List

from src.domain.tool_edge import ToolEdge


class RetrievalPlanParserPort(ABC):

    @abstractmethod
    def parse(self, edge_str: str) -> List[ToolEdge]:
        """
        Parses an LLM-generated JSON string into a list of ToolEdge objects.
        """
        pass