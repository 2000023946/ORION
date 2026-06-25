from src.domain.retrieval_step import RetrievalStep
from src.domain.result_item import ResultItem
from abc import ABC, abstractmethod

class ToolExecutionPort(ABC):
    @abstractmethod
    def execute(self, step: RetrievalStep) -> ResultItem:
        pass