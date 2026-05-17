"""Инлайн-клавиатуры для пагинации"""

from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.core.callbacks import BaseCallbackFactory
from bot.core.constants import (
    CALLBACK_IGNORE,
    PAGINATION_MAX_PAGES_ON_LINE,
)


def get_pagination_pages_keyboard(
    current_page: int,
    total_pages: int,
    section_prefix: str,
    back_to_years_callback: str,
    back_to_menu_callback: str,
):
    """
    Пагинация: [⬅️] [1/10] [➡️] + [🔙 Годы]
    """
    callbacks = BaseCallbackFactory(section_prefix)
    builder = InlineKeyboardBuilder()
    pagination_buttons = 1

    # Ряд 1: Навигация по страницам
    if current_page > 0:
        builder.button(
            text="⬅️ Назад",
            callback_data=callbacks.callback_pagination(current_page - 1),
        )
        pagination_buttons += 1

    builder.button(
        text=f"{current_page + 1}/{total_pages}",
        callback_data=CALLBACK_IGNORE,
    )

    if current_page < total_pages - 1:
        builder.button(
            text="Вперед ➡️",
            callback_data=callbacks.callback_pagination(current_page + 1),
        )
        pagination_buttons += 1

    # Ряд 2: Кнопка возврата к выбору года и возврат в меню
    builder.button(
        text="🔙 Годы",
        callback_data=back_to_years_callback,
    )
    builder.button(text="🔙 В меню", callback_data=back_to_menu_callback)
    builder.adjust(pagination_buttons, 2)

    return builder.as_markup()


def get_pagination_numbers_keyboard(
    current_page: int,
    total_pages: int,
    section_prefix: str,
    back_to_years_callback: str,
    back_to_menu_callback: str,
):
    """Альтернативная пагинация с номерами страниц"""
    callbacks = BaseCallbackFactory(section_prefix)

    builder = InlineKeyboardBuilder()

    for i in range(total_pages):
        if i == current_page:
            builder.button(
                text=f"🏁 Стр. {i + 1} 🏁", callback_data=CALLBACK_IGNORE
            )
        else:
            builder.button(
                text=f"Стр. {i + 1}",
                callback_data=callbacks.callback_pagination(i),
            )

    # Кнопка возврата к выбору года
    builder.button(text="🔙 Годы", callback_data=back_to_years_callback)
    builder.button(text="🔙 В меню", callback_data=back_to_menu_callback)
    builder.adjust(min(PAGINATION_MAX_PAGES_ON_LINE, total_pages), 2, 1)

    return builder.as_markup()


__all__ = ["get_pagination_pages_keyboard", "get_pagination_numbers_keyboard"]
