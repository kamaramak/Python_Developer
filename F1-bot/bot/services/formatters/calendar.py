"""Форматирование сообщений для Telegram"""

from datetime import datetime
from datetime import timedelta as td
from operator import itemgetter

import emoji

from bot.core.constants import (
    COUNTRIES,
    DATETIME_FORMAT_INP,
    DATETIME_FORMAT_OUT,
    DATETIME_FORMAT_SMALL_INP,
    DATETIME_FORMAT_SMALL_OUT,
    EMOJI_FLAGS,
    EVENTS,
    EVENTS_FOR_REMAINING_TIME,
    NATIONALITY_TO_COUNTRY,
    UTC,
    UTC_DELTA,
)

from .base import format_russian_text
from .translator import translate


async def format_race_header(
    round: int,
    city: str,
    country: str,
    circuit_name: str,
) -> str:
    """Форматирование заголовка этапа"""
    city_ru = await translate(city)
    country_ru = await translate(country)
    country_ru = COUNTRIES.get(country_ru, country_ru)
    country_ru = NATIONALITY_TO_COUNTRY.get(country_ru.lower(), country_ru)
    circuit_name_ru = await translate(circuit_name)
    country_flag = emoji.emojize(
        f"{EMOJI_FLAGS[country_ru]}", language="alias"
    )

    return (
        f"<b>{country_flag}ЭТАП {round}. {city_ru.upper()}, "
        f"{country_ru.upper()}\n"
        f"{circuit_name_ru.upper()}</b>"
    )


def format_event_line(
    event: str,
    dt: datetime,
    is_small: bool,
    laps: int = None,
) -> str:
    """Форматирование строки события"""
    now_dt = datetime.now(UTC)
    line = ""

    if now_dt > dt:
        line += "✅"
    dt += td(hours=UTC_DELTA)
    if is_small:
        line += f"{dt.strftime(DATETIME_FORMAT_SMALL_OUT)} {EVENTS[event]}"
    else:
        line += f"{dt.strftime(DATETIME_FORMAT_OUT)} {EVENTS[event]}"

    if event == "race" and laps is not None:
        ru_laps = format_russian_text(laps, "круг", "круга", "кругов")
        line += f" ({laps} {ru_laps})"

    return line


async def format_remaining_time(events: list) -> str:
    now_dt = datetime.now(UTC)
    for event, event_dt, _ in events:
        if event_dt > now_dt:
            remaining_time: td = event_dt - now_dt
            event_text = EVENTS_FOR_REMAINING_TIME[event]
            break
    else:
        return ""
    days = remaining_time.days
    hours = remaining_time.seconds // 3600
    minutes = (remaining_time.seconds % 3600) // 60
    days_text = (
        format_russian_text(days, "день", "дня", "дней")
        if days < 10
        else "дней"
    )
    hours_text = (
        format_russian_text(hours, "час", "часа", "часов")
        if hours < 10
        else "часов"
    )
    minutes_text = format_russian_text(minutes, "минута", "минуты", "минут")
    return (
        f"До {event_text} осталось:\n"
        f"{days} {days_text}, {hours} {hours_text} "
        f"и {minutes} {minutes_text}"
    )


async def sort_events(weekend_schedule: dict) -> list:
    """Сортировка событий уик-энда по времени"""
    events = []
    for event, dt_data in weekend_schedule.items():
        data_date = dt_data["date"]
        data_time = dt_data["time"]
        is_small = False
        if data_date is None and data_time is None:
            continue
        elif data_date is not None and data_time is None:
            dt = datetime.strptime(f"{data_date}", DATETIME_FORMAT_SMALL_INP)
            is_small = True
        else:
            dt = datetime.strptime(
                f"{data_date} {data_time}", DATETIME_FORMAT_INP
            )
        dt = dt.replace(tzinfo=UTC)
        events.append((event, dt, is_small))

    events.sort(key=itemgetter(1))
    return events


__all__ = ["format_race_header", "format_event_line", "sort_events"]
