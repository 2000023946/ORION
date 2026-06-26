from src.ports.llm_port import LLMPort
from src.ports.http_port import HttpPort

from src.domain.query import Query
from src.domain.retrieval_plan import RetrievalPlan
from src.domain.search_answer import SearchAnswer
from src.ports.tool_execution_port import ToolExecutionPort


class LLMAdapter(LLMPort):

    def __init__(self, http_port: HttpPort, config):
        self.http = http_port
        self.config = config

    def create_plan(self, query: Query, tools: list[ToolExecutionPort]) -> RetrievalPlan:

        # 1. Build tool descriptions for LLM
        tool_descriptions = [
            tool.describe().__dict__ for tool in tools
        ]

        # 2. Call LLM planning endpoint
        response = self.http.post(
            url=self.config.LLM_PLAN_API,
            body={
                "query": query.text,
                "tools": tool_descriptions
            }
        )

        # 3. Convert response → RetrievalPlan
        return RetrievalPlan.from_dict(response)

    def synthesize(self, query: Query, results: list) -> SearchAnswer:

        response = self.http.post(
            url=self.config.LLM_SYNTHESIS_API,
            body={
                "query": query.text,
                "results": [
                    r.__dict__ if hasattr(r, "__dict__") else r
                    for r in results
                ]
            }
        )

        return SearchAnswer.from_dict(response)