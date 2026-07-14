from src.domain.search_answer import SearchAnswer
from src.infrastructure.real.mcp_client.llm.llm_port import LLMPort
from src.infrastructure.real.mcp_client.llm.llm_response import LLMResponse
from src.infrastructure.real.mcp_client.parsing.retrieval_plan_parser_port import RetrievalPlanParserPort
from src.infrastructure.real.mcp_client.planning.prompt import Prompt
from src.domain.retrieval_plan import RetrievalPlan
from src.domain.query import Query
from src.domain.tool import Tool
from src.domain.context import Context
from src.infrastructure.real.mcp_client.planning.prompt_factory_port import PromptFactoryPort
from src.metrics.decorator import measure
from src.ports.mcp_client_port import MCPClientPort

from src.domain.tool_edge import ToolEdge


class RealMCPClient(MCPClientPort):
    def __init__(
            self, 
            llm_plan: LLMPort, 
            llm_answer: LLMPort,
            prompt_factory: PromptFactoryPort, 
            plan_parser: RetrievalPlanParserPort
        ):
        self.llm_plan = llm_plan
        self.llm_answer = llm_answer
        self.prompt_factory = prompt_factory
        self.plan_parser = plan_parser
    
    @measure("mcp_plan")
    async def create_plan(self, query: Query, tools: list[Tool]) -> RetrievalPlan:
        prompt: Prompt = self.prompt_factory.create_plan_prompt(query, tools)
        llm_output: LLMResponse = await self.llm_plan.generate(prompt)
        json_output = llm_output.get_response()
        
        tool_edges: list[ToolEdge] = self.plan_parser.parse(json_output)
        
                
        plan: RetrievalPlan = RetrievalPlan(tool_edges)
        
        return plan
        
    @measure("mcp_answer")
    async def answer(self, query: Query, context: Context) -> SearchAnswer:
        prompt = self.prompt_factory.create_answer_prompt(query, context)

        response: LLMResponse = await self.llm_answer.generate(prompt)

        return SearchAnswer(answer=response.get_response())