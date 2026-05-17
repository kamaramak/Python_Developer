from bot.core import cache
from bot.core.constants import (
    KEYBOARD_CURRENT_VERSION,
    KEYBOARD_USER_VERSION_KEY,
)


async def get_user_keyboard_version(user_id: int) -> str:
    """Получает версию клавиатуры пользователя"""
    version = await cache.get(f"{KEYBOARD_USER_VERSION_KEY}:{user_id}")
    return version or "0.0"


async def set_user_keyboard_version(
    user_id: int, version: str = KEYBOARD_CURRENT_VERSION
):
    """Сохраняет версию клавиатуры пользователя"""
    await cache.set(
        f"{KEYBOARD_USER_VERSION_KEY}:{user_id}", version, ttl=None
    )


async def needs_keyboard_update(user_id: int) -> bool:
    """Проверяет, нужно ли обновить клавиатуру"""
    user_version = await get_user_keyboard_version(user_id)
    return user_version != KEYBOARD_CURRENT_VERSION
