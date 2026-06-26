from src.domain.retrieval_plan import RetrievalPlan
from src.domain.search_answer import SearchAnswer
from src.ports.tool_execution_port import ToolExecutionPort
from src.domain.query import Query
from abc import ABC, abstractmethod

class LLMPort(ABC):
    @abstractmethod
    def create_plan(self, query: Query, tools: list[ToolExecutionPort]) -> RetrievalPlan:
        pass
    
    @abstractmethod
    def synthesize(self, query: Query, results: list) -> SearchAnswer:
        pass