from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot.config import SUPPORT_USERNAME
from bot.core.constants import CALLBACK_IGNORE

router = Router()


@router.callback_query(F.data == CALLBACK_IGNORE)
async def ignore_callback(callback: CallbackQuery):
    """Игнорируем нажатия на неактивные кнопки"""
    await callback.answer(cache_time=60)


@router.message(F.text == "💬 Связаться с разработчиком")
async def bug_report(message: Message):
    await message.answer(
        text=(
            "🛠 <b>Нашли ошибку?</b>\n\n"
            "Пожалуйста, напишите мне в личные сообщения:\n"
            f"👉 @{SUPPORT_USERNAME}\n\n"
            "При описании укажите:\n"
            "• Что вы хотели сделать\n"
            "• Что пошло не так\n"
            "• Скриншот (если есть)\n\n"
            "Спасибо за помощь в улучшении бота! 🏆"
        ),
        parse_mode="HTML",
    )
