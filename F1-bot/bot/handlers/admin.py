from datetime import datetime as dt
from datetime import timedelta as td

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.config import ADMIN_ID
from bot.core import cache
from bot.core.constants import USER_DATA_PREFIX, UTC
from bot.core.user_tracker import get_all_users, get_users_count

router = Router()


def is_admin(user_id: int) -> bool:
    """Проверка того, что пользователь является админом."""
    return user_id == ADMIN_ID


@router.message(Command("userstats"))
async def cmd_stats(message: Message):
    """Отображение статистики использования ботв (только для админа)."""
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Эта команда только для администратора")
        return

    users_list = await get_all_users()
    total_users = await get_users_count()

    now = dt.now(UTC)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = now - td(days=7)

    active_today = 0
    active_week = 0

    for user_entry in users_list:
        # Парсим ID из строки "123 - username"
        user_id = user_entry.split(" - ")[0]

        # Получаем детальные данные
        user_key = f"{USER_DATA_PREFIX}:{user_id}"
        user_data = await cache.get(user_key)

        if user_data:
            last_seen = dt.fromisoformat(user_data["last_seen"])

            if last_seen >= today_start:
                active_today += 1
            if last_seen >= week_ago:
                active_week += 1

    response = (
        f"📊 <b>Статистика бота</b>\n\n"
        f"👥 Всего пользователей: <b>{total_users}</b>\n"
        f"📍 Активных сегодня: <b>{active_today}</b>\n"
        f"🗓 Активных за неделю: <b>{active_week}</b>\n"
    )

    await message.answer(
        response,
        parse_mode="HTML",
    )


@router.message(Command("userlist"))
async def cmd_user_list(message: Message):
    """Отображение списка последних пользователей."""
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Эта команда только для администратора")
        return

    users = await get_all_users()

    if not users:
        await message.answer("📭 Пока нет пользователей")
        return

    # Показываем последних 20
    last_20 = users[-20:]

    text = "<b>Последние пользователи:</b>\n\n"
    for user_id in last_20:
        text += f"• `{user_id}`\n"

    await message.answer(
        text,
        parse_mode="HTML",
    )


@router.message(Command("userinfo"))
async def cmd_userinfo(message: Message):
    """Детальная информация о пользователе по ID"""
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Эта команда только для администратора")
        return

    args = message.text.split()
    if len(args) < 2:
        await message.answer("Использование: /userinfo <user_id>")
        return

    try:
        user_id = int(args[1])
    except ValueError:
        await message.answer("❌ Некорректный ID")
        return

    # Получаем детальные данные
    user_key = f"{USER_DATA_PREFIX}:{user_id}"
    user_data = await cache.get(user_key)

    if not user_data:
        await message.answer("❌ Пользователь не найден")
        return

    text = (
        f"📋 <b>Информация о пользователе</b>\n\n"
        f"🆔 ID: `{user_data['user_id']}`\n"
        f"👤 Имя: {user_data.get('first_name', '—')}\n"
        f"📝 Username: @{user_data.get('username', '—')}\n"
        f"🕐 Первый раз: {user_data['first_seen'][:16]}\n"
        f"🕐 Последний раз: {user_data['last_seen'][:16]}"
    )

    await message.answer(text, parse_mode="HTML")
