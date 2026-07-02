import pytest  # type: ignore
from unittest.mock import patch, MagicMock

from src.infrastructure.real.mcp_server.tools.vector_search.sentence_transformer_embedding import (
    SentenceTransformerEmbedding,
)


# -------------------------
# FIX: mock SentenceTransformer globally
# -------------------------
class FakeModel:
    def encode(self, inputs, convert_to_numpy=True, normalize_embeddings=False):

        if isinstance(inputs, str):
            return [0.1, 0.2, 0.3]

        return [
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6],
        ]


@pytest.fixture
def embedding():
    with patch(
        "src.infrastructure.real.mcp_server.tools.vector_search.sentence_transformer_embedding.SentenceTransformer"
    ) as MockST:

        MockST.return_value = FakeModel()

        emb = SentenceTransformerEmbedding(model_name="any-model")
        yield emb


# -------------------------
# SINGLE EMBEDDING
# -------------------------
def test_embed_single(embedding):

    result = embedding.embed("hello world")

    assert isinstance(result, list)
    assert len(result) == 3
    assert all(isinstance(x, float) for x in result)


# -------------------------
# BATCH EMBEDDING
# -------------------------
def test_embed_batch(embedding):

    result = embedding.embed_batch(["a", "b"])

    assert len(result) == 2
    assert all(len(v) == 3 for v in result)


# -------------------------
# TYPE CHECK
# -------------------------
def test_embedding_returns_floats(embedding):

    result = embedding.embed("test")

    assert all(isinstance(x, float) for x in result)