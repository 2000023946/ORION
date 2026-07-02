from src.application.search_response import SearchResponse
from src.domain.search_answer import SearchAnswer


def test_search_response_success():
    answer = SearchAnswer("This is the answer")

    response = SearchResponse(
        success=True,
        answer=answer,
        error=None,
    )

    assert response.success is True
    assert response.answer == answer
    assert response.error is None


def test_search_response_failure():
    response = SearchResponse(
        success=False,
        answer=None,
        error="Something went wrong",
    )

    assert response.success is False
    assert response.answer is None
    assert response.error == "Something went wrong"


def test_search_response_default_optional_fields():
    response = SearchResponse(success=True)

    assert response.success is True
    assert response.answer is None
    assert response.error is None