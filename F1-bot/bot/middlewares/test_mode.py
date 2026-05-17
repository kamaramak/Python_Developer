# middlewares/test_mode.py
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from bot.config import ADMIN_ID, DEBUG, TESTER_ID


class TestModeMiddleware(BaseMiddleware):
    """
    Блокирует посторонних в тестовом режиме
    """

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        # Все допускаются к работе в продакш-боте
        if not DEBUG:
            return await handler(event, data)
        # Только админ и тестировщик допускается к работе в тестовом боте
        if event.from_user.id in (ADMIN_ID, TESTER_ID):
            return await handler(event, data)

        # В остальных случаях - отказ в доступе
        await event.answer(
            text=(
                "🧪 <b>Это тестовая версия</b>\n\n"
                "Пожалуйста, используйте основного бота"
            ),
            parse_mode="HTML",
        )
        return None
