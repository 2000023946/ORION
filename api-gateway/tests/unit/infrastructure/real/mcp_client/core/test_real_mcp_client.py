import pytest  # type: ignore

from src.infrastructure.real.mcp_client.core.real_mcp_client import RealMCPClient
from src.infrastructure.real.mcp_client.llm.llm_port import LLMPort
from src.infrastructure.real.mcp_client.llm.llm_response import LLMResponse
from src.domain.query import Query
from src.domain.tool import Tool
from src.domain.tool_name import ToolName
from src.domain.context import Context
from src.domain.search_answer import SearchAnswer
from src.domain.retrieval_plan import RetrievalPlan
from src.domain.tool_edge import ToolEdge
from src.infrastructure.real.mcp_client.parsing.retrieval_plan_parser_port import RetrievalPlanParserPort
from src.infrastructure.real.mcp_client.planning.prompt import Prompt
from src.infrastructure.real.mcp_client.planning.prompt_factory_port import PromptFactoryPort


# -------------------------
# FAKE LLM
# -------------------------
class FakeLLM(LLMPort):
    def __init__(self, plan_json: str, answer_text: str):
        self.plan_json = plan_json
        self.answer_text = answer_text
        self.called = 0

    async def generate(self, prompt):  # type: ignore
        self.called += 1

        # first call = plan
        if self.called == 1:
            return LLMResponse(raw=self.plan_json)

        # second call = answer
        return LLMResponse(raw=self.answer_text)


# -------------------------
# FAKE PROMPT FACTORY
# -------------------------
class FakePromptFactory(PromptFactoryPort):
    def create_plan_prompt(self, query, tools):  # type: ignore
        return type("Prompt", (), {"prompt": "plan prompt"})()

    def create_answer_prompt(self, query, context):  # type: ignore
        return type("Prompt", (), {"prompt": "answer prompt"})()

    def create_db_filter_prompt(self, query: Query) -> Prompt:
        return type("Prompt", (), {"prompt": "db filter prompt"})()  # type: ignore


# -------------------------
# FAKE PARSER
# -------------------------
class FakeParser(RetrievalPlanParserPort):
    def parse(self, edge_str: str):
        return [
            ToolEdge(
                source=ToolName("START"),
                to=ToolName("END")
            )
        ]


# -------------------------
# CREATE PLAN TEST
# -------------------------
@pytest.mark.asyncio  # type: ignore[misc]
async def test_create_plan_success():

    llm = FakeLLM(
        plan_json='{"edges": [["START","END"]]}',
        answer_text="ignored"
    )

    factory = FakePromptFactory()
    parser = FakeParser()

    client = RealMCPClient(llm, factory, parser)

    query = Query("hello")

    tools = [
        Tool(
            name=ToolName("tool1"),
            description="test",
            inputs=[],
            outputs=[]
        )
    ]

    plan = await client.create_plan(query, tools)

    assert isinstance(plan, RetrievalPlan)
    assert len(plan.edges) == 1
    assert plan.edges[0].source == ToolName("START")
    assert plan.edges[0].to == ToolName("END")


# -------------------------
# ANSWER TEST
# -------------------------
@pytest.mark.asyncio  # type: ignore[misc]
async def test_answer_success():

    llm = FakeLLM(
        plan_json="unused",
        answer_text="final answer"
    )

    factory = FakePromptFactory()
    parser = FakeParser()

    client = RealMCPClient(llm, factory, parser)

    query = Query("what is ai")
    context = Context()
    await client.create_plan(query,[Tool(ToolName("A"), "desc", [], [])])
    result = await client.answer(query, context)
    print(result)
    assert isinstance(result, SearchAnswer)
    assert result.answer == "final answer"


# -------------------------
# LLM FAILURE HANDLING
# -------------------------
@pytest.mark.asyncio  # type: ignore[misc]
async def test_answer_llm_error():

    class FailingLLM(LLMPort):
        async def generate(self, prompt):  # type: ignore
            return LLMResponse(raw="", error="LLM failed")

    factory = FakePromptFactory()
    parser = FakeParser()

    client = RealMCPClient(FailingLLM(), factory, parser)

    query = Query("x")
    context = Context()

    try:
        result = await client.answer(query, context)
        assert result.answer == ""
    except ValueError as e:
        assert "LLM failed" in str(e)