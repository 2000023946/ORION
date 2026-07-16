from redis.asyncio import Redis
from src.infrastructure.config.settings import settings
from src.infrastructure.real.bus.redis_search_task_bus import RedisSearchTaskBus

class TaskBusInfrastructure:
    def __init__(self):
        self.redis_client = Redis.from_url(settings.bus_target_address, decode_responses=True)
        self.task_bus = RedisSearchTaskBus(redis_client=self.redis_client)