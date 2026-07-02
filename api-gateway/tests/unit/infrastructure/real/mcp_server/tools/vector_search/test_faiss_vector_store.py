import pytest  # type: ignore

from src.infrastructure.real.mcp_server.tools.vector_search.faiss_vector_store import FaissVectorStore


# -------------------------
# SINGLE ADD + SEARCH
# -------------------------
def test_faiss_add_and_search_single():

    store = FaissVectorStore(dim=3)

    store.add("doc1", [1.0, 0.0, 0.0])
    store.add("doc2", [0.0, 1.0, 0.0])

    results = store.search([1.0, 0.0, 0.0], k=2)

    assert len(results) == 2

    assert "doc_id" in results[0]
    assert "score" in results[0]

    assert results[0]["doc_id"] in ["doc1", "doc2"]
    assert isinstance(results[0]["score"], float)


# -------------------------
# BATCH ADD
# -------------------------
def test_faiss_add_batch():

    store = FaissVectorStore(dim=2)

    store.add_batch(
        doc_ids=["a", "b"],
        vectors=[
            [1.0, 0.0],
            [0.0, 1.0]
        ]
    )

    results = store.search([1.0, 0.0], k=2)

    assert len(results) == 2
    assert any(r["doc_id"] == "a" for r in results)


# -------------------------
# SCORE NORMALIZATION CHECK
# -------------------------
def test_faiss_score_is_normalized():

    store = FaissVectorStore(dim=2)

    store.add("doc1", [1.0, 0.0])

    results = store.search([1.0, 0.0], k=1)

    score = results[0]["score"]

    assert 0.0 < score <= 1.0


# -------------------------
# RESET FUNCTION
# -------------------------
def test_faiss_reset():

    store = FaissVectorStore(dim=2)

    store.add("doc1", [1.0, 0.0])

    assert len(store.search([1.0, 0.0], k=1)) > 0

    store.reset()

    results = store.search([1.0, 0.0], k=1)

    # after reset, FAISS returns empty index behavior
    assert len(results) == 0


# -------------------------
# INVALID BATCH SHAPE
# -------------------------
def test_faiss_invalid_batch_shape():

    store = FaissVectorStore(dim=2)

    with pytest.raises(ValueError):
        store.add_batch(
            doc_ids=["a"],
            vectors=[1.0, 2.0]  # invalid shape (not 2D)
        )