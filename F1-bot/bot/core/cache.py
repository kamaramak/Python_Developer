"""Кэширование для fetcher.py"""

import json
from datetime import datetime as dt
from datetime import timedelta as td
from typing import Any, Optional

import redis.asyncio as redis

from bot.config import REDIS_URL, TEST_REDIS_URL
from bot.core.constants import UTC


class CacheInterface:
    """Абстрактный базовый интерфейс кеша."""

    async def get(self, key: str) -> Optional[Any]:
        raise NotImplementedError

    async def set(self, key: str, value: Any, ttl: int):
        raise NotImplementedError

    async def delete(self, key: str) -> bool:
        """Удаляет ключ из кеша. Возвращает True если ключ существовал."""
        raise NotImplementedError


class RedisCache(CacheInterface):
    """Кеширование через Redis"""

    def __init__(self, testing: bool = False):
        redis_url = TEST_REDIS_URL if testing else REDIS_URL
        self.client = redis.from_url(redis_url, decode_responses=True)

    async def get(self, key: str) -> Optional[Any]:
        value = await self.client.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(self, key: str, value: Any, ttl: int) -> Optional[Any]:
        await self.client.set(key, json.dumps(value), ex=ttl)

    async def delete(self, key: str) -> bool:
        """Удаляет ключ из Redis."""
        result = await self.client.delete(key)
        return result > 0


class LocalCache(CacheInterface):
    """Локальное кеширование через словари."""

    def __init__(self):
        self._cache = {}
        self._expires = {}

    async def get(self, key: str) -> Optional[Any]:
        if key in self._expires:
            if dt.now(UTC) > self._expires[key]:
                del self._cache[key]
                del self._expires[key]
                return None
        return self._cache.get(key)

    async def set(self, key: str, value: Any, ttl: int):
        self._cache[key] = value
        if ttl is not None:
            self._expires[key] = dt.now(UTC) + td(seconds=ttl)

    async def delete(self, key: str) -> bool:
        """Удаляет ключ из локального кеша."""
        existed = key in self._cache
        self._cache.pop(key, None)
        self._expires.pop(key, None)
        return existed


def create_cache(testing: bool = False, local: bool = False) -> CacheInterface:
    """
    Фабрика создания кеша
    Args:
        local: True для локальной разработки (без Redis)
        testing: True для тестового Redis, False для боевого Redis
    """
    if local:
        print("📍 Используется локальный кеш (словарь)")
        return LocalCache()
    else:
        print("🌐 Используется Redis")
        return RedisCache(testing=testing)


_cache_instance: Optional[CacheInterface] = None


async def init_cache(testing: bool = False, local: bool = False):
    """Инициализация кеша."""
    global _cache_instance
    _cache_instance = create_cache(testing=testing, local=local)


async def get(key: str) -> Optional[Any]:
    """Получение значения из кеша."""
    if _cache_instance is None:
        raise RuntimeError(
            "Кеш не инициализирован! Сначала вызовите init_cache()"
        )
    return await _cache_instance.get(key)


async def set(key: str, value: Any, ttl: int):
    if _cache_instance is None:
        raise RuntimeError(
            "Кеш не инициализирован! Сначала вызовите init_cache()"
        )
    await _cache_instance.set(key, value, ttl)


async def delete(key: str) -> bool:
    """Удаляет ключ из кеша. Возвращает True если ключ существовал."""
    if _cache_instance is None:
        raise RuntimeError(
            "Кеш не инициализирован! Сначала вызовите init_cache()"
        )
    return await _cache_instance.delete(key)


__all__ = [
    "init_cache",
    "get",
    "set",
    "delete",
]
