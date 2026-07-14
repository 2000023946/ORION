import pytest

from src.domain.query import Query
from src.infrastructure.real.mcp_server.tools.web_search.mock_web_search_client import (
    MockWebSearchClient,
)
from src.infrastructure.real.mcp_server.tools.web_search.web_search_response import (
    WebSearchResponse,
)


@pytest.mark.asyncio
async def test_mock_web_search_returns_response():
    client = MockWebSearchClient()

    query = Query(
        text="Is the stock market up or down today?"
    )

    response = await client.search(query)

    assert isinstance(response, WebSearchResponse)

    assert response.query == "Is the stock market up or down today?"

    assert response.results is not None
    assert len(response.results) == 5


@pytest.mark.asyncio
async def test_mock_web_search_results_have_expected_fields():
    client = MockWebSearchClient()

    query = Query(
        text="test query"
    )

    response = await client.search(query)

    first_result = response.results[0]

    assert first_result.title == "U.S. Stock Markets Today"
    assert first_result.url == "https://www.example.com/markets"
    assert first_result.snippet is not None
    assert first_result.score == 0.47957736


@pytest.mark.asyncio
async def test_mock_web_search_has_simulated_latency():
    import time

    client = MockWebSearchClient()

    query = Query(
        text="latency test"
    )

    start = time.perf_counter()

    await client.search(query)

    elapsed = time.perf_counter() - start

    # allow small timing variance
    assert elapsed >= 1.4