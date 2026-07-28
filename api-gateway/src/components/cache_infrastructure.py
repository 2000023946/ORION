from redis.asyncio import Redis, ConnectionPool
from src.infrastructure.config.settings import settings
from src.infrastructure.real.bus.redis_search_task_bus import RedisSearchTaskBus
from src.infrastructure.real.cache.redis_cache_adapter import RedisCacheAdapter
from src.ports.cache import CachePort

class CacheInfrastructure:
    def __init__(self):
        # Create a persistent TCP connection pool
        self.pool = ConnectionPool.from_url(
            settings.cache_target_address, 
            max_connections=500,  # Adjust pool size based on your gateway concurrency needs
            decode_responses=True
        )
        # Pass the pool to the Redis async client
        self.redis_client = Redis(connection_pool=self.pool)
        self.cache: CachePort = RedisCacheAdapter(redis_client=self.redis_client)