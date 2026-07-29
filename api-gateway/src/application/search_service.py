import asyncio
import logging
from traceback import print_exc

import uvloop

from src.metrics.decorator import measure
from src.application.bus.search_task_bus import SearchTaskBus
from src.application.search_use_case import SearchUseCase
from src.application.bus.search_task_response import SearchTaskResponse

uvloop.install()


class SearchService:
    def __init__(
        self,
        use_case: SearchUseCase,
        task_bus: SearchTaskBus,
        max_workers: int = 300,  # 64 rps target * 3s per task
        queue_maxsize: int | None = None,
    ) -> None:
        self.use_case = use_case
        self.task_bus = task_bus
        self.max_workers = max_workers

        # Queue capped at max_workers: no benefit to buffering ahead of workers
        # since each task takes ~3s (I/O-bound), Redis round-trip time is
        # negligible in comparison. Keeps at most one task per worker in
        # memory at a time — minimizes what's lost on a crash, and avoids
        # hoarding tasks other pod replicas could pick up instead.
        self._internal_queue: asyncio.Queue = asyncio.Queue(
            maxsize=queue_maxsize or max_workers
        )
        self._is_running = False
        self._worker_tasks: list[asyncio.Task] = []

    async def execute(self):
        self._is_running = True

        self._worker_tasks = [
            asyncio.create_task(self._worker_loop(i))
            for i in range(self.max_workers)
        ]

        while self._is_running:
            try:
                free_capacity = self._internal_queue.maxsize - self._internal_queue.qsize()

                if free_capacity <= 0:
                    # Queue is completely full — no point pulling more from Redis
                    # right now. Short sleep since workers are actively draining
                    # and a slot could open any moment.
                    await asyncio.sleep(0.01)
                    continue

                tasks = await self.task_bus.pop_tasks(batch_size=free_capacity)

                if not tasks:
                    # Nothing in Redis. Scale sleep by how much free capacity we
                    # have: lots of room (queue mostly empty) means we're likely
                    # just waiting on new work arriving, so sleep longer to avoid
                    # hammering Redis. Little free room means the queue was
                    # recently near-full and workers are actively cycling, so
                    # check back sooner.
                    fullness_ratio = 1 - (free_capacity / self._internal_queue.maxsize)
                    sleep_time = 0.1 - (0.09 * fullness_ratio)  # ranges ~0.01 to 0.1
                    await asyncio.sleep(sleep_time)
                    continue

                for task in tasks:
                    await self._internal_queue.put(task)

            except asyncio.CancelledError:
                self._is_running = False
                break
            except Exception as e:
                logging.error(f"Error in execution loop polling tasks: {e}")
                await asyncio.sleep(0.1)
                print_exc()

    async def _worker_loop(self, worker_id: int):
        while self._is_running:
            try:
                task = await self._internal_queue.get()
                try:
                    await self._process_and_publish(task)
                finally:
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
                metadata=response.metadata,
            )

            await self.task_bus.publish(task_response)
        except Exception as e:
            logging.error(
                f"Task processing failed for request {getattr(task, 'request_id', 'unknown')}: {e}"
            )
            print_exc()

    def stop(self):
        self._is_running = False
        for worker in self._worker_tasks:
            worker.cancel()