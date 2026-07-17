from redis.asyncio import Redis
from src.infrastructure.config.settings import settings
from src.infrastructure.real.bus.redis_search_task_bus import RedisSearchTaskBus
from src.infrastructure.real.cache.redis_cache_adapter import RedisCacheAdapter
from src.ports.cache import CachePort

class CacheInfrastructure:
    def __init__(self):
        self.redis_client = Redis.from_url(settings.cache_target_address, decode_responses=True)
        self.cache: CachePort = RedisCacheAdapter(redis_client=self.redis_client)