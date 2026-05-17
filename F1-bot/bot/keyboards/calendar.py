from datetime import datetime as dt

from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.core.callbacks import CalendarCallbackFactory
from bot.core.constants import UTC


def calendar_menu_keyboard(section_prefix: str):
    decade = dt.now(UTC).year - (dt.now(UTC).year % 10)
    calendar_callbacks = CalendarCallbackFactory(section_prefix)
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🗓 Все сезоны",
        callback_data=calendar_callbacks.callback_all_years(decade),
    )
    builder.button(
        text=f"🗓 Календарь {dt.now(UTC).year}",
        callback_data=calendar_callbacks.callback_year(dt.now(UTC).year),
    )
    builder.button(
        text="⏭️ Ближайший Гран-При",
        callback_data=calendar_callbacks.calendar_current_race(),
    )
    builder.adjust(1)
    return builder.as_markup()


def calendar_current_race_keyboard(section_prefix: str):
    calendar_callbacks = CalendarCallbackFactory(section_prefix)
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔄 Обновить данные",
        callback_data=calendar_callbacks.calendar_current_race(),
    )
    builder.button(
        text="🔙 В меню",
        callback_data=calendar_callbacks.callback_back_to_menu(),
    )
    builder.adjust(1, 1)
    return builder.as_markup()
