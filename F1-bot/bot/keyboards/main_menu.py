"""Reply-клавиатура главного меню"""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Основное меню - только reply-клавиатура
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🗓 Календарь"),
            KeyboardButton(text="📊 Таблицы"),
            KeyboardButton(text="🏆 Результаты"),
        ],
        [KeyboardButton(text="🏁 Результаты крайней гонки")],
        [KeyboardButton(text="⏭️ Ближайший Гран-При")],
        [KeyboardButton(text="💬 Связаться с разработчиком")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите раздел...",
)

# Если понадобятся дополнительные reply-клавиатуры, добавляем их сюда же
__all__ = ["menu_keyboard"]
