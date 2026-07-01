from src.ports.mcp_client import MCPClient
from src.domain.retrieval_plan import RetrievalPlan, ToolEdge
from src.domain.query import Query
from src.domain.tool import Tool
from src.domain.context import Context


class DummyMCPClient(MCPClient):

    def create_plan(self, query: Query, tools: list[Tool]) -> RetrievalPlan:
        """
        Hardcoded DAG:
        search_user -> get_orders
        search_user -> get_profile
        get_orders -> generate_recommendation
        get_profile -> generate_recommendation
        """

        edges = [
            ToolEdge("search_user", "get_orders"),
            ToolEdge("search_user", "get_profile"),
            ToolEdge("get_orders", "generate_recommendation"),
            ToolEdge("get_profile", "generate_recommendation"),
        ]

        return RetrievalPlan(edges)

    def answer(self, query: Query, context: Context) -> Context:
        """
        Dummy synthesizer: just attaches a final answer string.
        """

        user = context.data.get("search_user", {})
        orders = context.data.get("get_orders", {})
        profile = context.data.get("get_profile", {})
        rec = context.data.get("generate_recommendation", {})

        context.data["final_answer"] = (
            f"User {user.get('name')} from {profile.get('location')} "
            f"has {len(orders.get('orders', []))} orders. "
            f"Recommendation: {rec.get('recommendation')}"
        )

        return context