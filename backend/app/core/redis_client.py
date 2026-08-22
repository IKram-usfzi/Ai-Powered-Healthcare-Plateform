import redis

from app.core.config import get_settings

settings = get_settings()
_redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)


def get_redis() -> redis.Redis:
    """docs/deccission.md ADR-002: Redis is scoped to dashboard KPI caching, alert
    de-duplication, and session/rate-limit state — not a general cache."""
    return _redis_client
