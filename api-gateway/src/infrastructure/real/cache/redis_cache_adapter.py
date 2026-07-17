import hashlib
import json
from typing import Optional
from redis.asyncio import Redis

from src.application.bus.search_task_response import SearchTaskResponse
from src.application.bus.request_id import RequestID
from src.domain.search_answer import SearchAnswer
from src.domain.query import Query
from src.ports.cache import CachePort


class RedisCacheAdapter(CachePort):
    def __init__(self, redis_client: Redis, ttl_seconds: int = 3600):
        """
        Args:
            redis_client: The async Redis connection.
            ttl_seconds: Time-to-live for cached items (default: 1 hour).
        """
        self.redis = redis_client
        self.ttl = ttl_seconds

    def _generate_key(self, query: Query) -> str:
        """
        Generates a deterministic Redis key based on the exact query text.
        We use SHA-256 hashing to ensure the key is safe and a consistent length.
        """
        query_string = query.text.lower().strip()
        query_hash = hashlib.sha256(query_string.encode('utf-8')).hexdigest()
        
        return f"cache:search:{query_hash}"

    async def get_answer(self, query: Query) -> Optional[SearchTaskResponse]:
        key = self._generate_key(query)
        cached_data = await self.redis.get(key)
        
        if not cached_data:
            return None
            
        # Decode the byte string from Redis if necessary
        if isinstance(cached_data, bytes):
            cached_data = cached_data.decode('utf-8')
            
        # Parse the JSON string into a dictionary
        data = json.loads(cached_data)
        
        # 1. Reconstruct RequestID from the flattened string
        req_id_val = data.get("request_id")
        if req_id_val is not None:
            data["request_id"] = RequestID(value=req_id_val)
            
        # 2. Reconstruct SearchAnswer from the flattened string
        answer_val = data.get("answer")
        if answer_val:  # If it's not an empty string or None
            # Assuming your SearchAnswer dataclass accepts 'answer' as its parameter
            # based on your to_dict() calling `self.answer.answer`
            data["answer"] = SearchAnswer(answer=answer_val)
        else:
            data["answer"] = None
            
        # Rebuild and return the full response object
        return SearchTaskResponse(**data)

    async def set_answer(self, query: Query, response: SearchTaskResponse) -> None:
        key = self._generate_key(query)
        
        # Serialize using your custom to_dict method
        response_json = json.dumps(response.to_dict())
        
        await self.redis.set(
            name=key, 
            value=response_json, 
            ex=self.ttl
        )