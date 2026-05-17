"""Универсальная клавиатура выбора года - ОДНА ДЛЯ ВСЕХ РАЗДЕЛОВ!"""

from datetime import datetime as dt
from typing import Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.core.callbacks import BaseCallbackFactory
from bot.core.constants import UTC


def get_years_keyboard(
    years: list[int],
    section_prefix: str,
    decade: int,
    value_type: Optional[str] = None,
):
    """
    🎯 ЕДИНАЯ клавиатура для ВСЕХ разделов:

    Аргументы:
        years: список годов
        section_prefix: префикс для callback (calendar/drivers/constructors)
        decade: первый год какой-то декады
    """
    callbacks = BaseCallbackFactory(section_prefix)
    builder = InlineKeyboardBuilder()
    max_decade = dt.now(UTC).year - (dt.now(UTC).year % 10)
    pagination_buttons = 1

    for year in years:
        text = f"{year}"
        callback_data = callbacks.callback_year(year, value_type)
        builder.button(text=text, callback_data=callback_data)

    if decade > 1950:
        text = f"⬇️{decade - 10}-ые⬇️"
        new_decade = decade - 10
        callback_data = callbacks.callback_all_years(new_decade)
        builder.button(text=text, callback_data=callback_data)
        pagination_buttons += 1

    builder.button(
        text="🔙 В меню", callback_data=callbacks.callback_back_to_menu()
    )

    if decade < max_decade:
        text = f"⬆️{decade + 10}-ые⬆️"
        new_decade = decade + 10
        callback_data = callbacks.callback_all_years(new_decade)
        builder.button(text=text, callback_data=callback_data)
        pagination_buttons += 1

    buttons = []
    if len(years) > 5:
        buttons.append(5)
        buttons.append(len(years) - 5)
    else:
        buttons.append(len(years))
    buttons.extend((pagination_buttons, 1))

    # Располагаем кнопки
    builder.adjust(*buttons)

    return builder.as_markup()


__all__ = ["get_years_keyboard"]
