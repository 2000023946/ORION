from abc import ABC, abstractmethod
from typing import List, Dict, Any


class VectorStorePort(ABC):
    """
    Abstract interface for vector search backends.
    """

    @abstractmethod
    def add(self, doc_id: str, vector: List[float]) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_batch(self, doc_ids: List[str], vectors: List[List[float]]) -> None:
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        query_vector: List[float],
        k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Returns:
            [
                {
                    "doc_id": str,
                    "score": float
                }
            ]
        """
        raise NotImplementedError
    
    @abstractmethod
    def reset(self) -> None:
        """
        Clears all stored vectors and state.
        """
        raise NotImplementedError