from abc import ABC, abstractmethod

from src.domain.retrieval_step import RetrievalStep
from src.domain.result_item import ResultItem


class ToolExecutionPort(ABC):

    @abstractmethod
    def execute(self, step: RetrievalStep) -> ResultItem:
        """Execute the tool using the provided retrieval step."""
        pass

    # @abstractmethod
    # def describe(self) -> str:
    #     """
    #     Returns a natural language description of the tool,
    #     including:
    #       - what the tool does
    #       - when it should be used
    #       - expected inputs
    #       - expected outputs
    #     """
    #     pass