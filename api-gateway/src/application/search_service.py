import asyncio
import uvloop
import logging
from traceback import print_exc

from src.application.bus.search_task_bus import SearchTaskBus
from src.application.search_use_case import SearchUseCase
from src.application.bus.search_task_response import SearchTaskResponse

# Swap the default asyncio event loop with the high-performance Cython/libuv engine
uvloop.install()

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
        # We move the actual processing into a separate helper method
        self._is_running = True
        
        while self._is_running:
            try:
                # 1. Poll task from the task bus
                task = await self.task_bus.pop_task()
                if not task:
                    continue
                
                # 2. Fire and forget! 
                # This schedules the work in the background and instantly moves to the next line.
                asyncio.create_task(self._process_and_publish(task))
                
                # 3. The loop instantly restarts and grabs the next task from Redis, 
                # even though the previous task is still waiting for the API!
                
            except asyncio.CancelledError:
                self._is_running = False
                break
            except Exception as e:
                logging.error(f"Error in execution loop polling tasks: {e}")
                print_exc()
            
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
            # Handle failure for this specific task
            logging.error(f"Task processing failed for request {getattr(task, 'request_id', 'unknown')}: {e}")
            print_exc()

        
    def stop(self):
        """Signals the worker to stop processing new tasks."""
        self._is_running = False