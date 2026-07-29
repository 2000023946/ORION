from redis.asyncio import Redis, ConnectionPool
from qdrant_client import AsyncQdrantClient
from src.infrastructure.config.settings import settings
from src.infrastructure.real.bus.redis_search_task_bus import RedisSearchTaskBus
from src.infrastructure.real.cache.qdrant_cache_adapter import QdrantCacheAdapter
from src.infrastructure.real.cache.redis_cache_adapter import RedisCacheAdapter
from src.ports.cache import CachePort

class CacheInfrastructure:
    def __init__(self, semantic_cache=True):
        # Create a persistent TCP connection pool
        self.pool = ConnectionPool.from_url(
            settings.cache_target_address, 
            max_connections=500,  # Adjust pool size based on your gateway concurrency needs
            decode_responses=True
        )
        
        if semantic_cache:
            self.qdrant_client = AsyncQdrantClient(url=settings.qdrant_target_address)
            self.cache: CachePort = QdrantCacheAdapter(
                qdrant_client=self.qdrant_client,
                embedding_target_address=settings.embedding_target_address,
                score_threshold=0.85  # Adjust similarity threshold as needed
            )
        else:
            # Pass the pool to the Redis async client
            self.redis_client = Redis(connection_pool=self.pool)
            self.cache: CachePort = RedisCacheAdapter(redis_client=self.redis_client)