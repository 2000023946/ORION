from abc import ABC, abstractmethod
from src.domain.retrieval_plan import RetrievalPlan
from src.ports.mcp_server_port import MCPServerPort
from src.domain.search_answer import SearchAnswer

class GraphExecutorPort(ABC):
    
    @abstractmethod
    async def execute(self, plan: RetrievalPlan, mcp_server: MCPServerPort) -> SearchAnswer:
        pass