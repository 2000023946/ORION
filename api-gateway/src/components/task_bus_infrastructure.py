from redis.asyncio import Redis, ConnectionPool
from src.infrastructure.config.settings import settings
from src.infrastructure.real.bus.redis_search_task_bus import RedisSearchTaskBus

class TaskBusInfrastructure:
    def __init__(self):
        # Create a persistent TCP connection pool for the task bus/broker
        self.pool = ConnectionPool.from_url(
            settings.bus_target_address, 
            max_connections=500,  # Adjust based on your worker and publisher load
            decode_responses=True
        )
        # Initialize the Redis client using the shared connection pool
        self.redis_client = Redis(connection_pool=self.pool)
        self.task_bus = RedisSearchTaskBus(redis_client=self.redis_client)
        