from flask_caching import Cache
from env_settings import redis_host, redis_port, redis_db

cache = Cache(
    config={
        "CACHE_TYPE": "RedisCache",
        "CACHE_REDIS_HOST": redis_host,
        "CACHE_REDIS_PORT": redis_port,
        "CACHE_REDIS_DB": redis_db
    }
)
