

from redis.asyncio import ConnectionPool, Redis
from app.core.config import settings

class RedisConnectionManager:
    def __init__(self):
        self._pool = None

    def get_pool(self) -> ConnectionPool:
        if self._pool is None:
            self._pool = ConnectionPool(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                max_connections=50
            )
        return self._pool

    async def close_pool(self) -> None:
        if self._pool:
            await self._pool.disconnect()
            self._pool = None

redis_manager = RedisConnectionManager()

async def get_redis_connection_pool() -> ConnectionPool:
    return redis_manager.get_pool()