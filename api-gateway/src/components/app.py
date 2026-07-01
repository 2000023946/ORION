from src.infrastructure.dummy.dummy_mcp_client import DummyMCPClient
from src.infrastructure.dummy.dummy_mcp_server import DummyMCPServer

from src.application.search_use_case import SearchUseCase
from src.domain.query import Query
from src.infrastructure.real.graph_executor.real_graph_executor import RealGraphExecuter


class App:
    def __init__(self):
        # infrastructure layer
        self.mcp_client = DummyMCPClient()
        self.mcp_server = DummyMCPServer()
        self.graph_executor = RealGraphExecuter()

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