from datetime import datetime as dt
from typing import Optional

from bot.core import cache
from bot.core.constants import USER_DATA_PREFIX, USER_SET_PREFIX, UTC


async def track_user(
    user_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
) -> None:
    """Сохраняет информацию и каждом пользователе."""
    users = await cache.get(USER_SET_PREFIX) or []
    user_short_data = f"{user_id} - {username}"
    if user_short_data not in users:
        users.append(user_short_data)
        await cache.set(USER_SET_PREFIX, users, ttl=None)

    user_key = f"{USER_DATA_PREFIX}:{user_id}"
    old_data = await cache.get(user_key) or {}

    user_data = {
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "last_seen": str(dt.now(UTC)),
        "first_seen": old_data.get("first_seen", str(dt.now(UTC))),
    }
    await cache.set(user_key, user_data, ttl=None)


async def get_users_count() -> int:
    users = await cache.get(USER_SET_PREFIX) or []
    return len(users)


async def get_all_users() -> list:
    return await cache.get(USER_SET_PREFIX) or []


async def get_user_info(user_id: int):
    user_key = f"{USER_DATA_PREFIX}:{user_id}"
    return await cache.get(user_key) or {}


async def delete_user_data(user_id: int):
    """Удаляет все данные пользователя."""
    user_key = f"{USER_DATA_PREFIX}:{user_id}"
    await cache.delete(user_key)

    users = await cache.get(USER_SET_PREFIX) or []
    users = [u for u in users if not u.startswith(str(user_id))]
    await cache.set(USER_SET_PREFIX, users, ttl=None)
