from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from bot.core.user_tracker import track_user


class UserTrackerMiddleware(BaseMiddleware):
    """
    Middleware для автоматической записи всех пользователей
    """

    async def __call__(
        self,
        handler: Callable[
            [Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]
        ],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        user = event.from_user

        await track_user(
            user_id=user.id, username=user.username, first_name=user.first_name
        )

        return await handler(event, data)
