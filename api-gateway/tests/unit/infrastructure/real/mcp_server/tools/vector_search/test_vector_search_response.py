from src.infrastructure.real.mcp_server.tools.vector_search.vector_search_response import VectorSearchResponse
from src.infrastructure.real.mcp_server.tools.vector_search.doc_id import DocId


# -------------------------
# BASIC SUCCESS CASE
# -------------------------
def test_vector_search_response_from_api_success():

    raw = {
        "matches": [
            {"doc_id": "doc1", "score": 0.9},
            {"doc_id": "doc2", "score": 0.8},
        ]
    }

    response = VectorSearchResponse.from_api(
        query="find similar docs",
        raw=raw
    )

    assert isinstance(response, VectorSearchResponse)
    assert response.query == "find similar docs"

    assert len(response.results) == 2

    assert response.results[0].doc_id == DocId("doc1")
    assert response.results[0].score == 0.9

    assert response.results[1].doc_id == DocId("doc2")
    assert response.results[1].score == 0.8


# -------------------------
# EMPTY MATCHES
# -------------------------
def test_vector_search_response_empty_matches():

    raw = {
        "matches": []
    }

    response = VectorSearchResponse.from_api(
        query="nothing",
        raw=raw
    )

    assert response.query == "nothing"
    assert response.results == []


# -------------------------
# MISSING FIELD SAFETY (expected failure case)
# -------------------------
def test_vector_search_response_missing_matches_key():

    raw = {}

    try:
        VectorSearchResponse.from_api(
            query="test",
            raw=raw
        )
        assert False, "Expected KeyError"
    except KeyError:
        assert True