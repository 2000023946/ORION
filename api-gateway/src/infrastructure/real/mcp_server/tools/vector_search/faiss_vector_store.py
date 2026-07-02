from typing import List, Dict, Any

import numpy as np
import faiss
from numpy.typing import NDArray

from src.infrastructure.real.mcp_server.tools.vector_search.vector_store_port import VectorStorePort



Vector = List[float]


class FaissVectorStore(VectorStorePort):
    """
    FAISS implementation with scoring.
    """

    def __init__(self, dim: int) -> None:
        self.dim: int = dim
        self.index: faiss.IndexFlatL2 = faiss.IndexFlatL2(dim)
        self.id_map: List[str] = []

    def add(self, doc_id: str, vector: Vector) -> None:
        vec: NDArray[np.float32] = np.asarray(vector, dtype=np.float32).reshape(1, self.dim)

        self.index.add(vec)
        self.id_map.append(doc_id)

    def add_batch(self, doc_ids: List[str], vectors: List[List[float]]) -> None:
        arr: NDArray[np.float32] = np.asarray(vectors, dtype=np.float32)

        if arr.ndim != 2:
            raise ValueError("Vectors must be 2D (N, dim)")

        self.index.add(arr)
        self.id_map.extend(doc_ids)

    def search(
        self,
        query_vector: Vector,
        k: int = 5
    ) -> List[Dict[str, Any]]:

        vec: NDArray[np.float32] = np.asarray(query_vector, dtype=np.float32).reshape(1, self.dim)

        distances: NDArray[np.float32]
        indices: NDArray[np.int64]

        distances, indices = self.index.search(vec, k)

        results: List[Dict[str, Any]] = []

        for i, idx in enumerate(indices[0]):
            if idx == -1:
                continue

            distance = float(distances[0][i])

            # convert L2 distance → similarity score (simple normalized version)
            score = 1 / (1 + distance)

            results.append({
                "doc_id": self.id_map[int(idx)],
                "score": score
            })

        return results
    
    def reset(self) -> None:
        self.index.reset()
        self.id_map = []