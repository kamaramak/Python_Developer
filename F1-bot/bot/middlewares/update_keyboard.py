from aiogram import BaseMiddleware

from bot.core.keyboard_version import (
    needs_keyboard_update,
    set_user_keyboard_version,
)
from bot.keyboards.main_menu import menu_keyboard


# middlewares/keyboard_version.py
class KeyboardVersionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user_id = event.from_user.id

        if await needs_keyboard_update(user_id):
            await event.answer(
                "🔄 <b>Меню бота обновлено!</b>\n"
                "Появились новые кнопки и функции.\n"
                "Пользуйтесь с удовольствием! 🏁",
                parse_mode="HTML",
                reply_markup=menu_keyboard,
            )
            await set_user_keyboard_version(user_id)

        return await handler(event, data)
