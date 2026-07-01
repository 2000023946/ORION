from src.domain.query import Query
from src.domain.search_answer import SearchAnswer
from src.domain.retrieval_plan import RetrievalPlan
from src.ports.graph_executer import GraphExecutor
from src.domain.context import Context
from src.domain.tool import Tool

from src.ports.mcp_client import MCPClient

from src.ports.mcp_server import MCPServer


class MCPOrchestrator:
    def __init__(
        self,
        mcp_client: MCPClient,
        mcp_server: MCPServer,
        graph_executor: GraphExecutor
    ):
        self.mcp_client = mcp_client
        self.mcp_server = mcp_server
        self.graph_executor = graph_executor

    async def run(self, query: Query) -> SearchAnswer:
        # 1. fetch available tools (domain boundary)
        tools: list[Tool] = self.mcp_server.get_tools()

        # 2. LLM creates DAG-based retrieval plan
        plan: RetrievalPlan = self.mcp_client.create_plan(query, tools)
        
        # 3. execute DAG (PARALLEL + dependency-aware)
        context: Context = await self.graph_executor.execute(plan, self.mcp_server)

        # 4. synthesize final answer using ALL results
        answer: SearchAnswer = self.mcp_client.answer(
            query=query,
            context=context
        )

        return answer