import pytest  # type: ignore
import dataclasses

from src.infrastructure.real.mcp_server.tools.vector_search.embedding import Embedding



# -------------------------
# CREATION TEST
# -------------------------
def test_embedding_creation():

    emb = Embedding(values=[0.1, 0.2, 0.3])

    assert emb.values == [0.1, 0.2, 0.3]


# -------------------------
# DIMENSION TEST
# -------------------------
def test_embedding_dimension():

    emb = Embedding(values=[0.1, 0.2, 0.3, 0.4])

    assert emb.dimension() == 4


# -------------------------
# IMMUTABILITY TEST
# -------------------------
def test_embedding_is_frozen():

    emb = Embedding(values=[0.1, 0.2])

    with pytest.raises(dataclasses.FrozenInstanceError):  # type: ignore[misc]
        emb.values = [1.0, 2.0] # type: ignore


# -------------------------
# EMPTY EMBEDDING EDGE CASE
# -------------------------
def test_embedding_empty_values():

    emb = Embedding(values=[])

    assert emb.dimension() == 0


# -------------------------
# TYPE CONSISTENCY
# -------------------------
def test_embedding_values_type():

    emb = Embedding(values=[1.0, 2.0])

    assert isinstance(emb.values, list)
    assert all(isinstance(x, float) for x in emb.values)