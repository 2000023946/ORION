from src.domain.search_answer import SearchAnswer
from src.infrastructure.real.mcp_client.llm.llm_port import LLMPort
from src.infrastructure.real.mcp_client.llm.llm_response import LLMResponse
from src.infrastructure.real.mcp_client.parsing.retrieval_plan_parser import RetrievalPlanParser
from src.infrastructure.real.mcp_client.planning.prompt import Prompt
from src.infrastructure.real.mcp_client.planning.prompt_factory import PromptFactory
from src.domain.retrieval_plan import RetrievalPlan
from src.domain.query import Query
from src.domain.tool import Tool
from src.domain.context import Context
from src.ports.mcp_client_port import MCPClientPort

from src.domain.tool_edge import ToolEdge


class RealMCPClient(MCPClientPort):
    def __init__(
            self, 
            llm: LLMPort, 
            prompt_factory: PromptFactory, 
            plan_parser: RetrievalPlanParser
        ):
        self.llm = llm
        self.prompt_factory = prompt_factory
        self.plan_parser = plan_parser
    
    async def create_plan(self, query: Query, tools: list[Tool]) -> RetrievalPlan:
        prompt: Prompt = self.prompt_factory.create_plan_prompt(query, tools)
        llm_output: LLMResponse = await self.llm.generate(prompt)
        
        json_output = llm_output.get_response()
        
        tool_edges: list[ToolEdge] = self.plan_parser.parse(json_output)
        
                
        plan: RetrievalPlan = RetrievalPlan(tool_edges)
        
        return plan
        
    
    async def answer(self, query: Query, context: Context) -> SearchAnswer:
        prompt = self.prompt_factory.create_answer_prompt(query, context)

        response: LLMResponse = await self.llm.generate(prompt)

        return SearchAnswer(answer=response.get_response())