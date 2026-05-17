from bot.core import cache
from bot.core.constants import (
    RESPONSE_CACHE_TTL,
)
from bot.core.http import get_response


async def get_response_or_cached(url, cache_key):
    cached = await cache.get(cache_key)
    if cached:
        response = cached
    else:
        response = await get_response(url)
        await cache.set(cache_key, response, RESPONSE_CACHE_TTL)
    return response
