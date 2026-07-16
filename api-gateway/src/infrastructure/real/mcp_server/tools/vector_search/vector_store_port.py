from abc import ABC, abstractmethod
from typing import List, Dict, Any


class VectorStorePort(ABC):
    """
    Abstract interface for asynchronous vector search backends.
    """

    @abstractmethod
    async def add(self, doc_id: str, vector: List[float]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def add_batch(self, doc_ids: List[str], vectors: List[List[float]]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def search(
        self,
        query_vector: Any,  # 'Any' allows the adapter to catch and convert Numpy arrays
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
    async def reset(self) -> None:
        """
        Clears all stored vectors and state.
        """
        raise NotImplementedError