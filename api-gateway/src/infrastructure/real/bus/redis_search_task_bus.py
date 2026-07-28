import json
import asyncio
from redis.asyncio import Redis
from redis.asyncio.client import PubSub

from src.application.bus.search_task_bus import SearchTaskBus
from src.application.bus.request_id import RequestID
from src.application.bus.search_task import SearchTask
from src.application.bus.search_task_response import SearchTaskResponse
from src.domain.query import Query
from src.domain.search_answer import SearchAnswer

class RedisSearchTaskBus(SearchTaskBus):
    def __init__(
        self, 
        redis_client: Redis, 
        queue_name: str = "queue:search_tasks", 
        channel_prefix: str = "channel:search_results"
    ):
        self._redis = redis_client
        self._queue_name = queue_name
        self._channel_prefix = channel_prefix

    @property
    def queue_name(self) -> str:
        return self._queue_name
    
    @property
    def channel(self) -> str:
        return self._channel_prefix

    async def push_task(self, search_task: SearchTask) -> RequestID:
        """Gateway pushes a task to the queue."""
        payload = {
            "request_id": search_task.request_id.value,
            "query_text": search_task.query.text 
        }
        
        # [DEBUG PRINT]
        # print(f"[DEBUG] Pushing task to queue '{self.queue_name}': {payload}", flush=True)
        
        await self._redis.lpush(self.queue_name, json.dumps(payload))
        
        # [DEBUG PRINT]
        # print(f"[DEBUG] Successfully pushed task {search_task.request_id.value}", flush=True)
        
        return search_task.request_id

    async def pop_task(self) -> SearchTask | None:
        """Pulls a task from the queue. Returns None if empty after 1 second."""
        # Change timeout from 0 to 1
        result = await self._redis.brpop(self.queue_name, timeout=1)
        
        if result:
            _, raw_payload = result
            data = json.loads(raw_payload)
            
            # [DEBUG PRINT]
            # print(f"[DEBUG] Popped task from queue '{self.queue_name}': {data['request_id']}", flush=True)
            
            return SearchTask(
                request_id=RequestID(value=data["request_id"]),
                query=Query(text=data["query_text"]) 
            )
            
        # Return None gracefully instead of crashing
        return None

    async def publish(self, result: SearchTaskResponse) -> None:
        """Worker broadcasts the completed task response."""
        specific_channel = f"{self.channel}:{result.request_id.value}"
        
        payload = {
            "request_id": result.request_id.value,
            "success": result.success,
            "answer_text": result.answer.answer if result.answer else None,
            "error": getattr(result, "error", None),
            "metadata": result.metadata
        }
        
        # [DEBUG PRINT]
        # print(f"[DEBUG] Publishing response to channel '{specific_channel}'", flush=True)
        
        await self._redis.publish(specific_channel, json.dumps(payload))

    async def subscribe(self, request_id: RequestID, timeout_seconds: float = 60.0) -> SearchTaskResponse:
        """Gateway listens for the result. Raises a TimeoutError if breached."""
        specific_channel = f"{self.channel}:{request_id.value}"
        pubsub: PubSub = self._redis.pubsub()
        
        try:
            # [DEBUG PRINT]
            # print(f"[DEBUG] Subscribing to channel '{specific_channel}'", flush=True)
            
            await pubsub.subscribe(specific_channel)
            
            async with asyncio.timeout(timeout_seconds):
                async for message in pubsub.listen():
                    # Ignore standard Redis subscription confirmation messages
                    if message["type"] == "message":
                        data = json.loads(message["data"])
                        
                        # [DEBUG PRINT]
                        # print(f"[DEBUG] Received message on channel '{specific_channel}'", flush=True)
                        
                        return SearchTaskResponse(
                            request_id=RequestID(value=data["request_id"]),
                            success=data["success"],
                            answer=SearchAnswer(answer=data["answer_text"]) if data["answer_text"] else None,
                            error=data.get("error"),
                            metadata=data.get("metadata")
                        )
                
                # FIX: Satisfy the type checker by handling the impossible loop exit
                raise RuntimeError("Redis PubSub loop exited unexpectedly without a message.")
                        
        except TimeoutError:
            # [DEBUG PRINT]
            # print(f"[DEBUG] Subscription timed out for channel '{specific_channel}'", flush=True)
            raise TimeoutError(f"Task {request_id.value} did not complete within {timeout_seconds} seconds.")
            
        finally:
            # Safely release the connection back to the pool
            await pubsub.unsubscribe(specific_channel)
            await pubsub.close()