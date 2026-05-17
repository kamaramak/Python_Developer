from datetime import datetime as dt

from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.core.callbacks import (
    ResultsCallbackFactory,
)
from bot.core.constants import (
    API_URL,
    EVENTS_FOR_RESULTS,
    RESULTS_PREFIX,
    UTC,
)
from bot.services.base import get_response_or_cached
from bot.services.formatters.results import format_results_round_keyboard


def results_menu_keyboard(section_prefix: str):
    decade = dt.now(UTC).year - (dt.now(UTC).year % 10)
    results_callbacks = ResultsCallbackFactory(section_prefix)
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🗓 Все сезоны (🏁 Гонки)",
        callback_data=results_callbacks.callback_all_years(decade),
    )
    for race_id, race_type in EVENTS_FOR_RESULTS.items():
        builder.button(
            text=f"{race_type}",
            callback_data=results_callbacks.callback_year(
                year=-1,
                value_type=race_id,
            ),
        )
    builder.adjust(1, 3, 2, 2)
    return builder.as_markup()


async def get_results_round_keyboard(section_prefix: str, year: int):
    results_callbacks = ResultsCallbackFactory(section_prefix)
    url = f"{API_URL}{year}"
    cache_key = f"{RESULTS_PREFIX}:{year}"
    response = await get_response_or_cached(url=url, cache_key=cache_key)
    races = response["races"]
    builder = InlineKeyboardBuilder()
    for race in races:
        round = race["round"]
        country = race["circuit"]["country"]
        text = await format_results_round_keyboard(round, country)
        callback_data = results_callbacks.callback_year(year, round)
        builder.button(text=text, callback_data=callback_data)
    decade = dt.now(UTC).year - (dt.now(UTC).year % 10)
    builder.button(
        text="🔙 Годы",
        callback_data=results_callbacks.callback_all_years(decade),
    )

    buttons = [2 for _ in range(len(races) // 2)]
    if len(races) % 2 == 1:
        buttons.append(1)
    buttons.append(1)
    builder.adjust(*buttons)
    return builder.as_markup()
