from src.components.graph_executor_infrastructure import GraphExecutorInfrastructure
from src.components.mcp_client_infrastructure import MCPClientInfrastructure
from src.components.mcp_server_infrastructure import MCPServerInfrastructure


from src.application.search_use_case import SearchUseCase
from src.domain.query import Query

class App:
    def __init__(self):
        # infrastructure layer
        self.mcp_server = MCPServerInfrastructure().mcp_server
        self.mcp_client = MCPClientInfrastructure().mcp_client
        self.graph_executor = GraphExecutorInfrastructure().graph_executor

        # application layer (use case)
        self.search_use_case = SearchUseCase(
            mcp_client=self.mcp_client,
            mcp_server=self.mcp_server,
            graph_executor=self.graph_executor
        )

    async def run(self, query_text: str):
        query = Query(text=query_text)

        result = await self.search_use_case.run(query)

        return result