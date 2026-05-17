from datetime import datetime as dt

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.config import SUPPORT_USERNAME
from bot.core.constants import UTC
from bot.core.user_tracker import delete_user_data, get_user_info
from bot.keyboards.main_menu import menu_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Приветствие и очистка состояния"""
    await state.clear()
    await message.answer(
        "🏎️ Привет! Я бот по Формуле 1!\n\n"
        "Я умею показывать:\n"
        "🗓 Календарь гонок\n"
        "📊 Турнирные таблицы (пилоты/конструкторы)\n"
        "🏆 Результаты сессий (квалификация, гонка, спринт)\n"
        "Выбери раздел в меню 👇",
        reply_markup=menu_keyboard,
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Помощь"""
    year = dt.now(UTC).year
    await message.answer(
        "🆘 Помощь по боту:\n\n"
        "Просто выбери нужный раздел в меню!\n"
        f"Доступны данные с 1950 по {year} год.\n\n"
        "Если что-то не работает - попробуй /start"
    )


@router.message(Command("privacy"))
async def cmd_privacy(message: Message):
    await message.answer(
        "🔐 <b>Политика конфиденциальности</b>\n\n"
        "Бот собирает минимальную информацию:\n"
        "• Ваш ID (для идентификации)\n"
        "• Username (если есть)\n"
        "• Имя (first name)\n"
        "• Время последнего обращения\n\n"
        "📊 Эти данные нужны только для статистики "
        "и улучшения работы бота.\n\n"
        "🗑 <b>Вы можете:</b>\n"
        "• Запросить копию своих данных — /export_my_data\n"
        "• Удалить все свои данные — /delete_my_data\n\n"
        "📌 С полной политикой конфиденциальности Вы можете ознакомиться "
        "в описании бота.\n\n"
        f"📬 Вопросы: @{SUPPORT_USERNAME}",
        parse_mode="HTML",
    )


@router.message(Command("export_my_data"))
async def cmd_export_my_data(message: Message):
    user_id = message.from_user.id
    user_data = await get_user_info(user_id)

    # Отправляем пользователю его данные
    await message.answer(
        f"📦 <b>Ваши данные:</b>\n\n"
        f"• ID: `{user_data['user_id']}`\n"
        f"• Username: @{user_data['username']}\n"
        f"• Имя: {user_data['first_name']}\n"
        f"• Первый раз: {user_data['first_seen']}\n"
        f"• Последний раз: {user_data['last_seen']}\n\n"
        "🔒 Эти данные нужны только для статистики\n"
        "🗑 Хотите удалить? Используйте /delete_my_data",
        parse_mode="HTML",
    )


@router.message(Command("delete_my_data"))
async def cmd_delete_my_data(message: Message):
    user_id = message.from_user.id

    # Удаляем данные пользователя
    await delete_user_data(user_id)  # твоя функция

    await message.answer(
        "✅ <b>Данные успешно удалены!</b>\n\n"
        "Все ваши личные данные стёрты из базы бота.\n"
        "Если вы снова воспользуетесь ботом, "
        "данные начнут собираться заново.\n\n"
        "Спасибо, что были с нами! 🏁",
        parse_mode="HTML",
    )
