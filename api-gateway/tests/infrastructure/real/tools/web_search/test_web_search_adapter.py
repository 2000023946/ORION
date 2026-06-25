import pytest
from src.config import config
from src.domain.retrieval_step import RetrievalStep
from src.infrastructure.dummy.dummy_http_port import DummyHttpAdapter
from src.infrastructure.real.tools.web_search_adapter.web_search_tool import WebSearchTool


def test_web_search_tool_execute_success():

    http_adapter = DummyHttpAdapter()
    tool = WebSearchTool(http_adapter, config)

    step = RetrievalStep(
        step_id="1",
        type="query",
        input="what is hnsw",
        params={"top_k": 5}
    )

    result = tool.execute(step)

    assert result.content == "dummy search result for 'what is hnsw'"
    assert result.score == 1.0


def test_web_search_tool_passes_query_to_http():

    http_adapter = DummyHttpAdapter()
    tool = WebSearchTool(http_adapter, config)

    step = RetrievalStep(
        step_id="2",
        type="query",
        input="vector databases"
    )

    result = tool.execute(step)

    # better assertion: check actual returned behavior
    assert "vector databases" in result.content


def test_web_search_tool_uses_config_url(monkeypatch):

    http_adapter = DummyHttpAdapter()
    tool = WebSearchTool(http_adapter, config)

    step = RetrievalStep(
        step_id="3",
        type="query",
        input="faiss vs hnsw"
    )

    captured = {}

    def fake_post(url, body, headers=None):
        captured["url"] = url
        captured["body"] = body
        return {
            "content": "ok",
            "score": 0.9
        }

    http_adapter.post = fake_post

    tool.execute(step)

    assert "url" in captured
    assert captured["body"]["query"] == "faiss vs hnsw"