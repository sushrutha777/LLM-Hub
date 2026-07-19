import time
import redis.asyncio as redis
from fastapi import HTTPException
from shared.config.settings import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def check_rate_limit(api_key: str, limit: int = 60, window: int = 60):
    """
    Simple fixed window rate limiting using Redis.
    Allows `limit` requests per `window` seconds.
    """
    key = f"rate_limit:{api_key}"
    
    try:
        current = await redis_client.get(key)
        if current is not None and int(current) >= limit:
            raise HTTPException(status_code=429, detail="Too Many Requests")
            
        async with redis_client.pipeline() as pipe:
            pipe.incr(key)
            if current is None:
                pipe.expire(key, window)
            await pipe.execute()
    except redis.ConnectionError:
        # If Redis is down, fail open (allow request) but log error
        import logging
        logging.error("Redis connection failed during rate limit check.")
