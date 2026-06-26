import pytest

from src.domain.retrieval_step import RetrievalStep
from src.infrastructure.dummy.dummy_http_port import DummyHttpAdapter
from src.infrastructure.real.tools.vector_service.vector_search_tool import (
    VectorSearchTool,
)
from src.config import config


def test_vector_search_tool_execute_success():

    # Arrange
    http_adapter = DummyHttpAdapter()

    tool = VectorSearchTool(http_adapter, config)

    step = RetrievalStep(
        step_id="1",
        type="query",
        input="what is hnsw",
        params={"top_k": 5}
    )

    # Act
    result = tool.execute(step)

    # Assert
    assert result.content == "dummy search result for 'what is hnsw'"
    assert result.score == 1.0


def test_vector_search_tool_passes_query_to_http():

    # Arrange
    http_adapter = DummyHttpAdapter()

    tool = VectorSearchTool(http_adapter, config)

    step = RetrievalStep(
        step_id="2",
        type="query",
        input="vector databases"
    )

    # Act
    result = tool.execute(step)

    # Assert
    assert "vector databases" in result.content


def test_vector_search_tool_uses_vector_db_url():

    # Arrange
    http_adapter = DummyHttpAdapter()

    tool = VectorSearchTool(http_adapter, config)

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

    # Act
    tool.execute(step)

    # Assert
    assert captured["url"] == config.VECTOR_DB_API
    assert captured["body"]["query"] == "faiss vs hnsw"
    
def test_vector_search_tool_describe_is_stable_contract():
    http_adapter = DummyHttpAdapter()

    tool = VectorSearchTool(http_adapter, config)

    desc = tool.describe()

    assert isinstance(desc.name, str)
    assert isinstance(desc.description, str)
    assert isinstance(desc.inputs, list)
    assert isinstance(desc.outputs, list)

    assert len(desc.name) > 0
    assert len(desc.description) > 10
    assert len(desc.inputs) > 0
    assert len(desc.outputs) > 0