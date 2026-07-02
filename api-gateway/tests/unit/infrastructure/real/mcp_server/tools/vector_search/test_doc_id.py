import dataclasses

import pytest # type: ignore
from src.infrastructure.real.mcp_server.tools.vector_search.doc_id import DocId  # type: ignore



# -------------------------
# BASIC CREATION
# -------------------------
def test_doc_id_creation():

    doc = DocId(doc_id="abc123")

    assert doc.doc_id == "abc123"


# -------------------------
# IMMUTABILITY TEST
# -------------------------
def test_doc_id_is_frozen():

    doc = DocId(doc_id="abc123")

    with pytest.raises(dataclasses.FrozenInstanceError): # type: ignore
        doc.doc_id = "new_id" # type: ignore


# -------------------------
# EQUALITY TEST
# -------------------------
def test_doc_id_equality():

    a = DocId(doc_id="same")
    b = DocId(doc_id="same")
    c = DocId(doc_id="different")

    assert a == b
    assert a != c


# -------------------------
# TYPE CONSISTENCY
# -------------------------
def test_doc_id_type():

    doc = DocId(doc_id="xyz") # type: ignore

    assert isinstance(doc.doc_id, str) # type: ignore