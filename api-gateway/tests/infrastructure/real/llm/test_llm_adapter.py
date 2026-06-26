import pytest

from src.infrastructure.dummy.dummy_llm_port import DummyLLMPort
from src.domain.query import Query
from src.domain.tool_description import ToolDescription
from src.ports.tool_execution_port import ToolExecutionPort
from src.domain.search_answer import SearchAnswer


# ---------------------------
# Fake tool for testing
# ---------------------------
class FakeTool(ToolExecutionPort):

    def execute(self, step):
        return None

    def describe(self):
        return ToolDescription(
            name="Fake Tool",
            description="tool used for testing LLM planning",
            inputs=["query"],
            outputs=["result"]
        )


# ---------------------------
# Test: create_plan basic
# ---------------------------
def test_dummy_llm_create_plan_returns_plan():

    llm = DummyLLMPort()

    query = Query(text="find users")

    tools = [FakeTool()]

    plan = llm.create_plan(query, tools)

    assert plan is not None
    assert hasattr(plan, "steps")
    assert len(plan.steps) > 0





# ---------------------------
# Test: synthesize returns SearchAnswer
# ---------------------------
def test_dummy_llm_synthesize_returns_search_answer():

    llm = DummyLLMPort()

    query = Query(text="what is AI")

    results = [
        {"content": "AI is machine intelligence", "score": 1.0}
    ]

    answer = llm.synthesize(query, results)

    assert isinstance(answer, SearchAnswer)
    assert isinstance(answer.answer, str)
    assert len(answer.answer) > 0


# ---------------------------
# Test: synthesize uses results
# ---------------------------
def test_dummy_llm_synthesize_includes_result_content():

    llm = DummyLLMPort()

    query = Query(text="explain ML")

    results = [
        {"content": "Machine learning is a subset of AI", "score": 0.9}
    ]

    answer = llm.synthesize(query, results)

    # Should reflect input context somehow (dummy behavior)
    assert "ML" in answer.answer or "machine" in answer.text.lower()