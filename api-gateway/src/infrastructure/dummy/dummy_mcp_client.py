from src.ports.mcp_client_port import MCPClientPort
from src.domain.retrieval_plan import RetrievalPlan, ToolEdge
from src.domain.query import Query
from src.domain.tool import Tool
from src.domain.context import Context
from src.domain.search_answer import SearchAnswer


class DummyMCPClient(MCPClientPort):

    async def create_plan(self, query: Query, tools: list[Tool]) -> RetrievalPlan:
        """
        Hardcoded DAG:
        search_user → get_orders
        search_user → get_profile
        get_orders → generate_recommendation
        get_profile → generate_recommendation
        """

        edges = [
            ToolEdge("search_user", "get_orders"),
            ToolEdge("search_user", "get_profile"),
            ToolEdge("get_orders", "generate_recommendation"),
            ToolEdge("get_profile", "generate_recommendation"),
        ]

        return RetrievalPlan(edges)

    async def answer(self, query: Query, context: Context) -> SearchAnswer:
        """
        Dummy synthesizer: builds final answer from execution context.
        """

        user = context.get("search_user") or {}
        orders = context.get("get_orders") or {}
        profile = context.get("get_profile") or {}
        rec = context.get("generate_recommendation") or {}

        final_answer = (
            f"User {user.get('name')} from {profile.get('location')} "
            f"has {len(orders.get('orders', []))} orders. "
            f"Recommendation: {rec.get('recommendation')}"
        )
        
        return SearchAnswer(answer=final_answer)