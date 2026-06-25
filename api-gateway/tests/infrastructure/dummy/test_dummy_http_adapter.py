from src.infrastructure.dummy.dummy_http_port import DummyHttpAdapter


def test_get_returns_expected_response():
    adapter = DummyHttpAdapter()

    response = adapter.get(
        url="https://example.com/search"
    )

    assert response["url"] == "https://example.com/search"
    assert response["method"] == "GET"
    assert response["content"] == "dummy get response"
    assert response["score"] == 1.0


def test_post_returns_expected_response():
    adapter = DummyHttpAdapter()

    body = {
        "query": "what is hnsw"
    }

    response = adapter.post(
        url="https://example.com/search",
        body=body
    )

    assert response["url"] == "https://example.com/search"
    assert response["method"] == "POST"
    assert response["request_body"] == body
    assert response["content"] == "dummy search result for 'what is hnsw'"
    assert response["score"] == 1.0


def test_post_handles_missing_query():
    adapter = DummyHttpAdapter()

    response = adapter.post(
        url="https://example.com/search",
        body={}
    )

    assert response["content"] == "dummy search result for ''"
    assert response["score"] == 1.0