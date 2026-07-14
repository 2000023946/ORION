import pytest

from src.domain.query import Query
from src.infrastructure.real.http.http_client_port import HttpClientPort
from src.infrastructure.real.http.http_response import HttpResponse
from src.infrastructure.real.mcp_server.tools.web_search.http_web_search_client import (
    HttpWebSearchClient,
)


class MockHttpClient(HttpClientPort):

    def __init__(self):
        self.last_url = None
        self.last_json = None

    async def post(
        self,
        url,
        data=None,
        json=None,
        headers=None,
        timeout=None,
    ):
        self.last_url = url
        self.last_json = json

        return HttpResponse(
            status_code=200,
            headers={
                "content-type": "application/json"
            },
            body={
                "query": "Is the stock market up or down today?",
                "results": [
                    {
                        "title": "Market Update",
                        "url": "https://example.com",
                        "snippet": "Market is up today",
                        "score": 0.95
                    }
                ],
                "answer": None
            }
        )

    async def get(self, *args, **kwargs):
        raise NotImplementedError

    async def put(self, *args, **kwargs):
        raise NotImplementedError

    async def delete(self, *args, **kwargs):
        raise NotImplementedError


@pytest.mark.asyncio
async def test_http_web_search_client_returns_response():

    mock_http = MockHttpClient()

    client = HttpWebSearchClient(mock_http)

    query = Query(
        text="Is the stock market up or down today?"
    )

    response = await client.search(query)

    assert response.query == "Is the stock market up or down today?"

    assert len(response.results) == 1

    assert response.results[0].title == "Market Update"

    assert response.results[0].url == "https://example.com"


@pytest.mark.asyncio
async def test_http_web_search_client_sends_correct_payload():

    mock_http = MockHttpClient()

    client = HttpWebSearchClient(mock_http)

    query = Query(
        text="test query"
    )

    await client.search(query)

    assert mock_http.last_json["query"] == "test query"

    assert "api_key" in mock_http.last_json

    assert mock_http.last_json["max_results"] == 5