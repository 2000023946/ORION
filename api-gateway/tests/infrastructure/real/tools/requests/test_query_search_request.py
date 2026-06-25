import pytest

from src.domain.query import Query
from src.domain.retrieval_step import RetrievalStep
from src.infrastructure.real.tools.requests.query_search_request import QuerySearchRequest


def test_from_retrieval_step_creates_request():
    step = RetrievalStep(
        step_id="1",
        type="query",
        input="python dataclasses",
        params={"top_k": 5}
    )

    request = QuerySearchRequest.from_retrieval_step(step)

    assert isinstance(request.query, Query)
    assert request.query.text == "python dataclasses"
    assert request.params == {"top_k": 5}


def test_from_retrieval_step_raises_for_wrong_type():
    step = RetrievalStep(
        step_id="1",
        type="query_a",
        input="python dataclasses"
    )

    with pytest.raises(ValueError) as exc_info:
        QuerySearchRequest.from_retrieval_step(step)

    assert "Expected step type 'query'" in str(exc_info.value)


def test_to_dict():
    request = QuerySearchRequest(
        query=Query("machine learning"),
        params={"limit": 10}
    )

    result = request.to_dict()

    assert result["query"] == request.query.text
    assert result["query"] == "machine learning"
    assert result["params"] == {"limit": 10}