from abc import ABC, abstractmethod

from src.application.bus.request_id import RequestID
from src.application.bus.search_task import SearchTask
from src.application.bus.search_task_response import SearchTaskResponse


class SearchTaskBus(ABC):
    
    @property
    @abstractmethod
    def queue_name(self) -> str: 
        """The specific inbox the workers pull from."""
        pass
    
    @property
    @abstractmethod
    def channel(self) -> str: 
        """The broadcast frequency the gateway listens to."""
        pass
    
    @abstractmethod
    async def push_task(self, search_task: SearchTask) -> RequestID:
        """Gateway pushes a task to the queue."""
        pass

    @abstractmethod
    async def pop_task(self) -> SearchTask | None:
        """Worker pulls a task from the queue. Should yield control to the event loop while waiting."""
        pass

    @abstractmethod
    async def subscribe(self, request_id: RequestID, timeout_seconds: float = 60.0) -> SearchTaskResponse:
        """Gateway listens for the result. Raises a TimeoutError if breached."""
        pass
    
    @abstractmethod
    async def publish(self, result: SearchTaskResponse) -> None:
        """Worker broadcasts the completed task response."""
        pass