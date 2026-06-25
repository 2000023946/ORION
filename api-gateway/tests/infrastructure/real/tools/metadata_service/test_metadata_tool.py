import pytest

from src.domain.retrieval_step import RetrievalStep
from src.domain.query import Query
from src.domain.result_item import ResultItem
from src.infrastructure.real.tools.metadata_service.metadata_tool import MetadataTool
from src.infrastructure.dummy.dummy_http_port import DummyHttpAdapter
from src.config import Config, config


def test_metadata_tool_execute_success():

    # Arrange
    http_adapter = DummyHttpAdapter()

    tool = MetadataTool(http_adapter, config)

    step = RetrievalStep(
        step_id="1",
        type="metadata",
        input="ignored",
        params={"ids": ["doc1", "doc2"]}
    )

    # Act
    result = tool.execute(step)

    # Assert
    assert isinstance(result, ResultItem)
    assert result.content.startswith("dummy")
    assert result.score == 1.0


def test_metadata_tool_sends_correct_url():

    http_adapter = DummyHttpAdapter()


    tool = MetadataTool(http_adapter, config)

    step = RetrievalStep(
        step_id="2",
        type="metadata",
        input="ignored",
        params={"ids": ["a", "b"]}
    )

    captured = {}

    def fake_post(url, body, headers=None):
        captured["url"] = url
        captured["body"] = body
        return {
            "content": "ok",
            "score": 0.8
        }

    http_adapter.post = fake_post

    tool.execute(step)

    assert captured["url"] == ""# since it defaults to this 
    assert captured["body"]["ids"] == ["a", "b"]


def test_metadata_tool_converts_request_correctly():

    http_adapter = DummyHttpAdapter()

    tool = MetadataTool(http_adapter, config)

    step = RetrievalStep(
        step_id="3",
        type="metadata",
        input="ignored",
        params={"ids": ["x1", "x2", "x3"]}
    )

    result = tool.execute(step)

    # ensure request pipeline worked end-to-end
    assert result.content is not None
    assert isinstance(result.score, float)