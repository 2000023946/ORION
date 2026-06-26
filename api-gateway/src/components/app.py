from src.domain.query import Query
from src.domain.search_answer import SearchAnswer

from src.application.mcp_orchestrator import MCPOrchestrator
from src.application.graph_executer import GraphExecutor

from src.infrastructure.real.http.requests_http_adapter import RequestsHttpAdapter
from src.infrastructure.real.llm.adapter.llm_adapter import LLMAdapter
from src.infrastructure.real.tools.registry.tool_registry import ToolRegistry

from src.config import config


class App:

    def __init__(self):

        # ---------------------------
        # Infrastructure
        # ---------------------------
        self.http = RequestsHttpAdapter()

        # ---------------------------
        # Core ports
        # ---------------------------
        self.llm = LLMAdapter(self.http, config)
        self.tool_registry = ToolRegistry(self.http, config)

        # ---------------------------
        # Execution engine
        # ---------------------------
        self.graph_executor = GraphExecutor(
            tool_registry=self.tool_registry
        )

        # ---------------------------
        # Orchestrator (USE CASE)
        # ---------------------------
        self.orchestrator = MCPOrchestrator(
            llm_port=self.llm,
            tool_registry_port=self.tool_registry,
            graph_executor=self.graph_executor
        )

    async def run(self, query_text: str) -> SearchAnswer:
        query = Query(text=query_text)
        return await self.orchestrator.run(query)