

# -------------------------
# basic creation
# -------------------------
from src.infrastructure.real.mcp_server.tools.db_filter.db_filter_response import DBFilterResponse


def test_db_filter_response_basic():

    raw = [
        {
            "_id": "1",
            "title": "doc1",
            "content": "hello",
            "price": "10",
            "metadata": {"a": 1},
        },
        {
            "_id": "2",
            "title": "doc2",
            "content": "world",
            "price": "20",
            "metadata": {"b": 2},
        },
    ]

    resp = DBFilterResponse.from_raw(raw)

    assert resp is not None
    assert len(resp.documents) == 2


# -------------------------
# field mapping sanity
# -------------------------
def test_db_filter_response_field_mapping():

    raw = [
        {
            "_id": "123",
            "title": "test-title",
            "content": "test-content",
            "price": "99",
            "metadata": {"x": 1},
        }
    ]

    resp = DBFilterResponse.from_raw(raw)

    doc = resp.documents[0]

    assert doc.doc_id == "123"
    assert doc.title == "test-title"
    assert doc.content == "test-content"
    assert doc.price == "99"


# -------------------------
# empty input safety
# -------------------------
def test_db_filter_response_empty():

    resp = DBFilterResponse.from_raw([])

    assert isinstance(resp.documents, list)
    assert len(resp.documents) == 0