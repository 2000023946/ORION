from src.infrastructure.real.mcp_server.tools.metadata_filter.metadata_response import MetadataResponse
from src.infrastructure.real.mcp_server.tools.metadata_filter.document import Document


# -------------------------
# BASIC CONVERSION
# -------------------------
def test_metadata_response_from_raw():

    raw = [
        {
            "_id": "doc1",
            "title": "A",
            "content": "content A",
            "price": "10",
            "metadata": {"tag": "x"}
        },
        {
            "_id": "doc2",
            "title": "B",
            "content": "content B",
            "price": "20",
            "metadata": {"tag": "y"}
        },
    ]

    response = MetadataResponse.from_raw(raw)

    assert isinstance(response, MetadataResponse)
    assert len(response.documents) == 2

    assert response.documents[0] == Document.from_raw(raw[0])
    assert response.documents[1] == Document.from_raw(raw[1])


# -------------------------
# EMPTY INPUT
# -------------------------
def test_metadata_response_empty_list():

    response = MetadataResponse.from_raw([])

    assert isinstance(response, MetadataResponse)
    assert response.documents == []


# -------------------------
# TYPE INTEGRITY
# -------------------------
def test_metadata_response_contains_documents():

    raw = [
        {"_id": "x"},
    ]

    response = MetadataResponse.from_raw(raw)

    assert isinstance(response.documents, list)
    assert all(isinstance(d, Document) for d in response.documents)