from src.domain.retrieval_step import RetrievalStep
from src.domain.retrieval_result import RetrievalResult
from abc import ABC, abstractmethod

class ToolExecutionPort(ABC):
    @abstractmethod
    def execute(self, step: RetrievalStep) -> RetrievalResult:
        pass