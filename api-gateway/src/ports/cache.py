from abc import ABC, abstractmethod
from typing import Optional

from src.application.bus.search_task_response import SearchTaskResponse
from src.domain.query import Query

class CachePort(ABC):
    """
    Abstract interface for caching LLM/Graph responses.
    """
    
    @abstractmethod
    async def get_answer(self, query: Query) -> Optional[SearchTaskResponse]:
        """Returns the cached response if it exists, otherwise None."""
        pass
        
    @abstractmethod
    async def set_answer(self, query: Query, response: SearchTaskResponse) -> None:
        """Saves the computed response to the cache."""
        pass