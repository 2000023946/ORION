from abc import ABC, abstractmethod
from src.domain.retrieval_plan import RetrievalPlan
from src.domain.query import Query
from src.domain.tool import Tool
from src.domain.context import Context

class MCPClientPort(ABC):
    
    @abstractmethod
    async def create_plan(self, query: Query, tools: list[Tool]) -> RetrievalPlan:
        pass
    
    @abstractmethod
    async def answer(self, query: Query, context: Context) -> Context:
        pass   
    