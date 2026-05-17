from datetime import datetime as dt

from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.core.callbacks import (
    ConstructorsCallbackFactory,
    DriversCallbackFactory,
)
from bot.core.constants import UTC


def standings_menu_keyboard(
    drivers_prefix: str,
    constructors_prefix: str,
):
    decade = dt.now(UTC).year - (dt.now(UTC).year % 10)
    constructors_callbacks = ConstructorsCallbackFactory(constructors_prefix)
    drivers_callbacks = DriversCallbackFactory(drivers_prefix)
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔧 Конструкторы (все сезоны)",
        callback_data=constructors_callbacks.callback_all_years(decade),
    )
    builder.button(
        text="👤 Пилоты (все сезоны)",
        callback_data=drivers_callbacks.callback_all_years(decade),
    )
    builder.button(
        text=f"🔧 Конструкторы ({dt.now(UTC).year})",
        callback_data=constructors_callbacks.callback_year(dt.now(UTC).year),
    )
    builder.button(
        text=f"👤 Пилоты ({dt.now(UTC).year})",
        callback_data=drivers_callbacks.callback_year(dt.now(UTC).year),
    )
    builder.adjust(1)
    return builder.as_markup()
