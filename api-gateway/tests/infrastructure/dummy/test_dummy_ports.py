import pytest
import asyncio
from src.infrastructure.dummy.dummy_tool_registry_port import DummyToolRegistryPort
from src.infrastructure.dummy.dummy_tool_execution_port import DummyToolExecutionPort
from src.infrastructure.dummy.dummy_llm_port import DummyLLMPort
from src.domain.retrieval_step import RetrievalStep
from src.domain.query import Query


def test_tool_registry_returns_tools():
    registry = DummyToolRegistryPort()

    tools = registry.get_tools()

    assert isinstance(tools, list)
    assert len(tools) == 3
    assert any(t["name"] == "semantic_search" for t in tools)
    



@pytest.mark.asyncio
async def test_tool_execution():
    executor = DummyToolExecutionPort()

    step = RetrievalStep(
        step_id="s1",
        type="semantic_search",
        input="AI",
        params={}
    )

    result = await executor.execute(step)

    assert result["step_id"] == "s1"
    assert result["type"] == "semantic_search"
    assert "output" in result
    


def test_llm_create_plan():
    llm = DummyLLMPort()

    query = Query(text="what is AI?")
    tools = [{"name": "semantic_search"}]

    plan = llm.create_plan(query, tools)

    assert plan.query == "what is AI?"
    assert len(plan.steps) == 3

    assert "s1" in plan.steps
    assert "s2" in plan.steps
    assert "s3" in plan.steps

    assert ("s1", "s3") in plan.edges
    assert ("s2", "s3") in plan.edges