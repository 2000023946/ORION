import pytest

from src.infrastructure.real.tools.requests.query_search_request import QuerySearchRequest
from src.domain.retrieval_step import RetrievalStep
from src.domain.query import Query


def test_from_retrieval_step_success():
    step = RetrievalStep(params={"query": "neural networks"})

    request = QuerySearchRequest.from_retrieval_step(step)

    assert isinstance(request, QuerySearchRequest)
    assert isinstance(request.query, Query)
    assert request.query.text == "neural networks"


def test_from_retrieval_step_missing_query_raises():
    step = RetrievalStep(params={})

    with pytest.raises(ValueError) as exc:
        QuerySearchRequest.from_retrieval_step(step)

    assert "expected query in params" in str(exc.value)


def test_to_dict_returns_correct_format():
    query = Query("machine learning")
    request = QuerySearchRequest(query=query)

    result = request.to_dict()

    assert result == {"query": "machine learning"}