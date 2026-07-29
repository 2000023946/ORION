import asyncio
from src.metrics.decorator import measure
import uvloop
import logging
from traceback import print_exc

from src.application.bus.search_task_bus import SearchTaskBus
from src.application.search_use_case import SearchUseCase
from src.application.bus.search_task_response import SearchTaskResponse

uvloop.install()

class SearchService:
    def __init__(self, use_case: SearchUseCase, task_bus: SearchTaskBus, max_workers: int = 200, queue_maxsize: int = 500) -> None:
        self.use_case = use_case
        self.task_bus = task_bus
        self.max_workers = max_workers
        
        # Internal buffer queue to hold tasks pulled from Redis safely
        self._internal_queue = asyncio.Queue(maxsize=queue_maxsize)
        self._is_running = False
        self._worker_tasks = []

    async def execute(self):
        self._is_running = True
        
        self._worker_tasks = [
            asyncio.create_task(self._worker_loop(i)) 
            for i in range(self.max_workers)
        ]
        
        while self._is_running:
            try:
                free_space = self._internal_queue.maxsize - self._internal_queue.qsize()
                
                if free_space > 0:
                    tasks = await self.task_bus.pop_tasks(batch_size=free_space)
                    
                    if not tasks:
                        await asyncio.sleep(0.1) 
                        continue
                    
                    for task in tasks:
                        await self._internal_queue.put(task)
                else:
                    # The queue is full. 
                    # Instead of sleeping 0.5s, yield control briefly. 
                    # The workers will process tasks and make space.
                    await asyncio.sleep(0.01)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(f"Error in execution loop: {e}")
    
    async def _worker_loop(self, worker_id: int):
        """Dedicated worker consumer pulling from the internal queue."""
        while self._is_running:
            try:
                # Wait for the next task to become available in our internal queue
                task = await self._internal_queue.get()
                
                try:
                    # Await directly so this worker stays busy and respects the concurrency limit
                    await self._process_and_publish(task)
                finally:
                    # Always mark the task as done so the queue tracks capacity correctly
                    self._internal_queue.task_done()
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(f"Worker {worker_id} encountered an error: {e}")

    @measure("SearchResponse")
    async def _process_and_publish(self, task):
        try:
            response = await self.use_case.run(task.query)
            
            task_response = SearchTaskResponse(
                request_id=task.request_id,
                answer=response.answer,
                success=response.success,
                error=response.error,
                metadata=response.metadata
            )
            
            await self.task_bus.publish(task_response)
        except Exception as e:
            logging.error(f"Task processing failed for request {getattr(task, 'request_id', 'unknown')}: {e}")
            print_exc()

    def stop(self):
        self._is_running = False
        # Cancel all active worker loops gracefully
        for worker in self._worker_tasks:
            worker.cancel()