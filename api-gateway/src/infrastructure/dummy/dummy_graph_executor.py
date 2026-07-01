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

        return Context(context)