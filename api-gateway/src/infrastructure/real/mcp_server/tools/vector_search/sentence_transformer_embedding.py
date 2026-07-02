from typing import List, Any

import numpy as np
from sentence_transformers import SentenceTransformer

from src.infrastructure.real.mcp_server.tools.vector_search.embedding_port import EmbeddingPort



Vector = List[float]


class SentenceTransformerEmbedding(EmbeddingPort):
    """
    Strict but safe embedding adapter.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.model: Any = SentenceTransformer(model_name)

    def embed(self, text: str) -> Vector:
        vec = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=False,
        )

        return np.asarray(vec, dtype=np.float32).tolist()

    def embed_batch(self, texts: List[str]) -> List[Vector]:
        vecs = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=False,
        )

        arr = np.asarray(vecs, dtype=np.float32)
        return [v.tolist() for v in arr]