from src.domain.query import Query
from src.domain.search_answer import SearchAnswer
from src.application.search_response import SearchResponse
from src.domain.retrieval_plan import RetrievalPlan
from src.ports.graph_executer_port import GraphExecutorPort
from src.domain.context import Context
from src.domain.tool import Tool

from src.ports.mcp_client_port import MCPClientPort
from src.ports.mcp_server_port import MCPServerPort


class SearchUseCase:
    def __init__(
        self,
        mcp_client: MCPClientPort,
        mcp_server: MCPServerPort,
        graph_executor: GraphExecutorPort
    ):
        self.mcp_client = mcp_client
        self.mcp_server = mcp_server
        self.graph_executor = graph_executor

    async def run(self, query: Query) -> SearchResponse:
        try:
            # 1. fetch available tools
            tools: list[Tool] = await self.mcp_server.get_tools()

            # 2. LLM creates DAG-based retrieval plan
            plan: RetrievalPlan = await self.mcp_client.create_plan(query, tools)

            # 3. execute DAG (PARALLEL + dependency-aware)
            context: Context = await self.graph_executor.execute(plan, self.mcp_server)

            # 4. synthesize final answer
            answer: SearchAnswer = await self.mcp_client.answer(
                query=query,
                context=context
            )

            return SearchResponse(
                success=True,
                answer=answer
            )

        except Exception as e:
            return SearchResponse(
                success=False,
                error=str(e)
            )