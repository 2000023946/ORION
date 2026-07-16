import asyncio
import logging
from traceback import print_exc

from src.application.bus.search_task_bus import SearchTaskBus
from src.application.search_use_case import SearchUseCase
from src.application.bus.search_task_response import SearchTaskResponse


class SearchService:
    def __init__(self, use_case: SearchUseCase, task_bus: SearchTaskBus) -> None:
        self.use_case = use_case
        self.task_bus = task_bus
        self._is_running = False 
    
    async def execute(self):
        """
        Starts the infinite worker loop to consume tasks from the queue 
        and process them through the Search Use Case.
        """
        self._is_running = True
        print(f"Worker started. Listening to queue: {self.task_bus.queue_name}")
        
        while self._is_running:
            try:
                
                # 1. Poll task from the task bus (yields control to event loop while empty)
                task = await self.task_bus.pop_task()
                print("got a task recieved", task)
                if not task:
                    continue
                    
                print(f"Processing RequestID: {task.request_id.value}")
                
                # 2. Call the Use Case
                response = await self.use_case.run(task.query)
                # 3. Construct the Response payload for the Bus
                # Note: We extract the answer from the SearchResponse domain object.
                task_response = SearchTaskResponse(
                    request_id=task.request_id,
                    answer=response.answer,
                    success=response.success,
                    error=response.error,
                    metadata=response.metadata
                )
                
                # 4. Publish the result back to the Gateway
                await self.task_bus.publish(task_response)
                print(f"Published result for RequestID: {task.request_id.value}")
                
            except asyncio.CancelledError:
                # Allows the worker to shut down gracefully when Kubernetes terminates the pod
                print("Worker shutting down gracefully.")
                self._is_running = False
                break
            except Exception as e:
                # Catch unexpected errors so the worker doesn't crash permanently
                print(f"Critical error in worker loop: {str(e)}")
                # (Optional but recommended: publish a failure response back to the Gateway here)

    def stop(self):
        """Signals the worker to stop processing new tasks."""
        self._is_running = False