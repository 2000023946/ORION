from abc import ABC, abstractmethod
from src.domain.context import Context
from src.domain.retrieval_plan import RetrievalPlan
from src.ports.mcp_server_port import MCPServerPort

class GraphExecutorPort(ABC):
    
    @abstractmethod
    async def execute(self, plan: RetrievalPlan, mcp_server: MCPServerPort) -> Context:
        pass