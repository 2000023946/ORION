from typing import Any

from src.domain.query import Query
from src.domain.tool_name import ToolName
from src.ports.graph_executer_port import GraphExecutorPort
from src.domain.retrieval_plan import RetrievalPlan
from src.ports.mcp_server_port import MCPServerPort
from src.domain.context import Context


class DummyGraphExecuter(GraphExecutorPort):

    async def execute(self, query: Query, plan: RetrievalPlan, mcp_server: MCPServerPort) -> Context:
        context: dict[ToolName, Any] = {}

        context[ToolName("search_user")] = "mock_user_123"
        context[ToolName("get_orders")] = "order_1, order_2, order_3"
        context[ToolName("get_profile")] = "name: John Doe, age: 21"
        context[ToolName("generate_recommendation")] = "recommend: product A, product B"

        return Context(context)