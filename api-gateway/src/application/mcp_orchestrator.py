from src.domain.query import Query
from src.domain.search_answer import SearchAnswer
from src.domain.retrieval_plan import RetrievalPlan
from src.ports.llm_port import LLMPort
from src.ports.tool_registry_port import ToolRegistryPort
from src.application.graph_executer import GraphExecutor


class MCPOrchestrator:
    def __init__(
        self,
        llm_port: LLMPort,
        tool_registry_port: ToolRegistryPort,
        graph_executor: GraphExecutor
    ):
        self.llm_port = llm_port
        self.tool_registry_port = tool_registry_port
        self.graph_executor = graph_executor

    async def run(self, query: Query) -> SearchAnswer:
        # 1. fetch available tools (domain boundary)
        tools = self.tool_registry_port.get_tools()

        # 2. LLM creates DAG-based retrieval plan
        plan: RetrievalPlan = self.llm_port.create_plan(query, tools)

        # 3. execute DAG (PARALLEL + dependency-aware)
        step_results: dict[str, any] = await self.graph_executor.execute(plan)

        # 4. synthesize final answer using ALL results
        answer: SearchAnswer = self.llm_port.synthesize(
            query=query,
            results=list(step_results.values())
        )

        return answer