from src.infrastructure.real.mcp_server.tools.vector_search.vector_search_result import VectorSearchResult
from src.infrastructure.real.mcp_server.tools.vector_search.doc_id import DocId


# -------------------------
# SINGLE RAW PARSE
# -------------------------
def test_vector_search_result_from_raw():

    raw = { # type: ignore
        "doc_id": "doc-123",
        "score": 0.85
    }

    result = VectorSearchResult.from_raw(raw) # type: ignore

    assert isinstance(result, VectorSearchResult)
    assert result.doc_id == DocId("doc-123")
    assert result.score == 0.85


# -------------------------
# SCORE COERCION TO FLOAT
# -------------------------
def test_vector_search_result_score_coercion():

    raw = {
        "doc_id": "doc-1",
        "score": "0.75"  # string input
    }

    result = VectorSearchResult.from_raw(raw)

    assert isinstance(result.score, float)
    assert result.score == 0.75


# -------------------------
# LIST PARSING
# -------------------------
def test_vector_search_result_from_raw_list():

    raw_list = [ # type: ignore
        {"doc_id": "a", "score": 0.9},
        {"doc_id": "b", "score": 0.8},
        {"doc_id": "c", "score": 0.7},
    ]

    results = VectorSearchResult.from_raw_list(raw_list) # type: ignore

    assert len(results) == 3

    assert results[0].doc_id == DocId("a")
    assert results[1].doc_id == DocId("b")
    assert results[2].doc_id == DocId("c")

    assert results[0].score == 0.9
    assert results[1].score == 0.8
    assert results[2].score == 0.7


# -------------------------
# EMPTY LIST EDGE CASE
# -------------------------
def test_vector_search_result_empty_list():

    results = VectorSearchResult.from_raw_list([])

    assert results == []