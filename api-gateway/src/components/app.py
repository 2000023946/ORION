from src.application.search_service import SearchService
from src.components.graph_executor_infrastructure import GraphExecutorInfrastructure
from src.components.mcp_client_infrastructure import MCPClientInfrastructure
from src.components.mcp_server_infrastructure import MCPServerInfrastructure

from src.application.search_use_case import SearchUseCase
from src.components.task_bus_infrastructure import TaskBusInfrastructure
from src.domain.query import Query

class App:
    def __init__(self, mock: bool = False):
        # infrastructure layer
        self.mcp_server_infras = MCPServerInfrastructure()
        self.mcp_client_infras = MCPClientInfrastructure()
        self.graph_executor_infras = GraphExecutorInfrastructure()
        self.task_bus_infras = TaskBusInfrastructure()
        if mock:
            self.mcp_client_infras.use_mock()
            self.mcp_server_infras.use_mock()

        # application layer (use case)
        self.search_use_case = SearchUseCase(
            mcp_client=self.mcp_client_infras.mcp_client,
            mcp_server=self.mcp_server_infras.mcp_server,
            graph_executor=self.graph_executor_infras.graph_executor
        )
        
        self.worker = SearchService(
            use_case=self.search_use_case, 
            task_bus=self.task_bus_infras.task_bus
        )

    async def run(self):
        await self.worker.execute()