from abc import ABC, abstractmethod
from typing import List


class EmbeddingPort(ABC):
    """
    Port (interface) for embedding models.
    """

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """
        Convert text into embedding vector.
        """
        pass

    @abstractmethod
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Convert multiple texts into embedding vectors.
        """
        pass
    
    