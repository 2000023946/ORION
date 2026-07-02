from typing import Any

from src.infrastructure.real.http.http_response import HttpResponse
from src.infrastructure.real.mcp_server.tools.web_search.web_search_response import WebSearchResponse


# -------------------------
# SUCCESS CASE
# -------------------------
def test_web_search_response_create_success():

    payload: dict[str, Any] = {
        "query": "ai",
        "answer": "AI is intelligence",
        "results": [
            {
                "title": "AI Article",
                "url": "https://example.com/ai",
                "content": "AI explained here",
                "score": 0.92
            }
        ]
    }

    response = HttpResponse(
        status_code=200,
        headers={},
        body=payload
    )

    result = WebSearchResponse.create(response)

    assert result.query == "ai"
    assert result.answer == "AI is intelligence"
    assert len(result.results) == 1

    first = result.results[0]
    assert first.title == "AI Article"
    assert first.url == "https://example.com/ai"
    assert first.snippet == "AI explained here"
    assert first.score == 0.92


# -------------------------
# SNIPPET FALLBACK (content → snippet)
# -------------------------
def test_web_search_response_snippet_fallback():

    payload: dict[str, Any] = {
        "query": "ai",
        "results": [
            {
                "title": "AI Article",
                "url": "https://example.com/ai",
                "snippet": "Direct snippet"
            }
        ]
    }

    response = HttpResponse(
        status_code=200,
        headers={},
        body=payload
    )

    result = WebSearchResponse.create(response)

    assert result.results[0].snippet == "Direct snippet"


# -------------------------
# CONTENT FALLBACK
# -------------------------
def test_web_search_response_content_fallback():

    payload: dict[str, Any] = {
        "query": "ai",
        "results": [
            {
                "title": "AI Article",
                "url": "https://example.com/ai",
                "content": "Fallback content"
            }
        ]
    }

    response = HttpResponse(
        status_code=200,
        headers={},
        body=payload
    )

    result = WebSearchResponse.create(response)

    assert result.results[0].snippet == "Fallback content"


# -------------------------
# EMPTY RESULTS
# -------------------------
def test_web_search_response_empty_results():

    payload: dict[str, Any] = {
        "query": "none",
        "results": []
    }

    response = HttpResponse(
        status_code=200,
        headers={},
        body=payload
    )

    result = WebSearchResponse.create(response)

    assert result.query == "none"
    assert result.results == []
    assert result.answer is None


# -------------------------
# MISSING FIELDS SAFETY
# -------------------------
def test_web_search_response_missing_fields():

    response = HttpResponse(
        status_code=200,
        headers={},
        body={}
    )

    result = WebSearchResponse.create(response)

    assert result.query == ""
    assert result.results == []
    assert result.answer is None