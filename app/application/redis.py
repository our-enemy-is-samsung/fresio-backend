import redis.asyncio as redis

from app.env_validator import get_settings

settings = get_settings()


class RedisConnection:
    def __init__(self):
        self._pool = redis.ConnectionPool.from_url(settings.REDIS_URI)

    def get_connection(self):
        return redis.Redis(connection_pool=self._pool)


redis_manager = RedisConnection()
