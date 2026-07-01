import pytest

from src.config import config
from src.domain.tool_type import ToolType
from src.domain.retrieval_step import RetrievalStep
from src.infrastructure.dummy.dummy_http_port import DummyHttpAdapter
from src.infrastructure.real.tools.web_search_adapter.web_search_tool import WebSearchTool


def test_web_search_tool_execute_success():

    http_adapter = DummyHttpAdapter()
    tool = WebSearchTool(http_adapter, config)

    step = RetrievalStep(
        tool_type=ToolType.WEB_SEARCH,
        params={"query": "what is hnsw", "top_k": 5}
    )

    result = tool.execute(step)

    assert result.content == "dummy search result for 'what is hnsw'"


def test_web_search_tool_passes_query_to_http():

    http_adapter = DummyHttpAdapter()
    tool = WebSearchTool(http_adapter, config)

    step = RetrievalStep(
        tool_type=ToolType.WEB_SEARCH,
        params={"query": "vector databases"}
    )

    result = tool.execute(step)

    assert "vector databases" in result.content


def test_web_search_tool_uses_config_url():

    http_adapter = DummyHttpAdapter()
    tool = WebSearchTool(http_adapter, config)

    step = RetrievalStep(
        tool_type=ToolType.WEB_SEARCH,
        params={"query": "faiss vs hnsw"}
    )

    captured = {}

    def fake_post(url, body, headers=None):
        captured["url"] = url
        captured["body"] = body
        return {"content": "ok", "score": 0.9}

    http_adapter.post = fake_post

    tool.execute(step)

    assert captured["url"] == config.WEB_API
    assert captured["body"]["query"] == "faiss vs hnsw"


def test_web_search_tool_describe_contract():

    http_adapter = DummyHttpAdapter()
    tool = WebSearchTool(http_adapter, config)

    desc = tool.describe()

    assert isinstance(desc.name, str)
    assert isinstance(desc.description, str)
    assert isinstance(desc.inputs, list)
    assert isinstance(desc.outputs, list)