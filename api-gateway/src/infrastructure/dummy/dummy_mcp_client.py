from src.domain.tool_name import ToolName
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
            ToolEdge(ToolName("search_user"), ToolName("get_orders")),
            ToolEdge(ToolName("search_user"), ToolName("get_profile")),
            ToolEdge(ToolName("get_orders"), ToolName("generate_recommendation")),
            ToolEdge(ToolName("get_profile"), ToolName("generate_recommendation")),
        ]

        return RetrievalPlan(edges)

    async def answer(self, query: Query, context: Context) -> SearchAnswer:
        """
        Dummy synthesizer: builds final answer from execution context.
        """


        user = context.get(ToolName("search_user"))
        orders = context.get(ToolName("get_orders"))
        profile = context.get(ToolName("get_profile"))
        rec = context.get(ToolName("generate_recommendation"))

        final_answer = (
            f"User {user.get('name')} from {profile.get('location')} "
            f"has {len(orders.get('orders', []))} orders. "
            f"Recommendation: {rec.get('recommendation')}"
        )
        
        return SearchAnswer(answer=final_answer)