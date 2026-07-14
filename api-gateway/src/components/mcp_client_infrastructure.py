from src.infrastructure.mock.mock_llm_answer import MockAnswerLLM
from src.infrastructure.mock.mock_llm_plan import MockPlanLLM
from src.infrastructure.real.http.http_client_port import HttpClientPort
from src.infrastructure.real.http.real_http_client import RealHttpClient
from src.infrastructure.real.mcp_client.core.real_mcp_client import RealMCPClient
from src.infrastructure.real.mcp_client.llm.llm import LLM
from src.infrastructure.real.mcp_client.llm.llm_port import LLMPort
from src.infrastructure.real.mcp_client.parsing.json_adapter import JsonAdapter
from src.infrastructure.real.mcp_client.parsing.retrieval_plan_parser import RetrievalPlanParser
from src.infrastructure.real.mcp_client.planning.prompt_factory import PromptFactory


class MCPClientInfrastructure:
    def __init__(self):
        self.http_client: HttpClientPort = RealHttpClient()
        self.json_parser: JsonAdapter = JsonAdapter()
        self.llm: LLMPort = LLM(http_client=self.http_client, json_parser=self.json_parser)
        self.prompt_factory: PromptFactory = PromptFactory()
        self.mock_plan_llm  = MockPlanLLM()
        self.mock_answer_llm = MockAnswerLLM()
        self.plan_parser = RetrievalPlanParser(json=self.json_parser)
        self.mcp_client = RealMCPClient(
            llm_plan=self.llm,
            llm_answer=self.llm,
            prompt_factory=self.prompt_factory,
            plan_parser=self.plan_parser
        )
        
    def use_mock(self):
        self.mcp_client.llm_plan = self.mock_plan_llm
        self.mcp_client.llm_answer = self.mock_answer_llm
        
    def use_real(self):
        self.mcp_client.llm_plan = self.llm
        self.mcp_client.llm_answer = self.llm
        
        
        
        