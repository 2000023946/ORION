import pytest

from src.domain.retrieval_step import RetrievalStep
from src.infrastructure.real.llm.prompts.filter_prompt import FilterTool
from src.infrastructure.dummy.dummy_http_port import DummyHttpAdapter
from src.config import config


def test_filter_tool_full_pipeline_success():

    http = DummyHttpAdapter()
    tool = FilterTool(http)

    step = RetrievalStep(
        step_id="1",
        type="filter",
        input="find active users",
        params={"table": "users"}
    )

    result = tool.execute(step)

    assert result.content != ""
    assert isinstance(result.score, float)


def test_filter_tool_calls_llm_then_db():

    http = DummyHttpAdapter()
    tool = FilterTool(http)

    step = RetrievalStep(
        step_id="2",
        type="filter",
        input="get users older than 30",
        params={}
    )

    calls = []

    def fake_post(url, body, headers=None):
        calls.append((url, body))

        # LLM call
        if url == config.SYNTHESIS_LLM:
            return {
                "content": "SELECT * FROM users WHERE age > 30",
                "score": 0.0
            }

        # DB call
        if url == config.FILTER_API:
            return {
                "content": "userA,userB",
                "score": 1.0
            }

        return {}

    http.post = fake_post

    result = tool.execute(step)

    # Assert call order
    assert calls[0][0] == config.SYNTHESIS_LLM
    assert calls[1][0] == config.FILTER_API

    # Assert SQL passed to DB
    assert "SELECT" in calls[1][1]["query"]

    # Assert final output
    assert result.content == "userA,userB"
    assert result.score == 1.0


def test_filter_tool_passes_query_and_params():

    http = DummyHttpAdapter()
    tool = FilterTool(http)

    step = RetrievalStep(
        step_id="3",
        type="filter",
        input="get orders",
        params={"limit": 10}
    )

    captured = {}

    def fake_post(url, body, headers=None):
        captured[url] = body
        return {
            "content": "ok",
            "score": 0.5
        }

    http.post = fake_post

    tool.execute(step)

    # LLM call validation
    assert config.SYNTHESIS_LLM in captured
    assert captured[config.SYNTHESIS_LLM]["query"] == "get orders"
    assert captured[config.SYNTHESIS_LLM]["params"]["limit"] == 10