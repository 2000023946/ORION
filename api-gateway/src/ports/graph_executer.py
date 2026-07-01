from abc import ABC, abstractmethod
from src.domain.retrieval_plan import RetrievalPlan
from src.ports.mcp_server import MCPServer
from src.domain.search_answer import SearchAnswer

class GraphExecutor(ABC):
    
    @abstractmethod
    def execute(self, plan: RetrievalPlan, mcp_server: MCPServer) -> SearchAnswer:
        pass