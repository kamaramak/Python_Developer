"""Сервис для работы с календарем гонок"""

from bot.core.constants import API_URL, CALENDAR_PREFIX, NO_DATA_ERROR

from .base import get_response_or_cached
from .formatters.calendar import (
    format_event_line,
    format_race_header,
    format_remaining_time,
    sort_events,
)


async def get_current_race() -> str:
    """Получение информации по ближайшей гонке"""
    url = f"{API_URL}current/next/"
    cache_key = f"{CALENDAR_PREFIX}:curren:next"
    response = await get_response_or_cached(url, cache_key)
    if response is None:
        return NO_DATA_ERROR
    message = "<b>⏭️ СЛЕДУЮЩИЙ ЭТАП:</b>\n"
    race = response["race"][0]
    header = await format_race_header(
        round=response["round"],
        city=race["circuit"]["city"],
        country=race["circuit"]["country"],
        circuit_name=race["circuit"]["circuitName"],
    )
    message += f"{header}\n"

    # Сортируем события
    events = await sort_events(race["schedule"])

    # Добавляем события
    for event, dt, is_small in events:
        line = format_event_line(
            event=event,
            dt=dt,
            is_small=is_small,
            laps=race.get("laps"),
        )
        if event == "qualy":
            message += "-" * 25 + "\n"
        message += f"{line}\n"
    message += "-" * 25 + "\n"
    remaining_time = await format_remaining_time(
        events=events,
    )
    message += remaining_time
    return message


async def get_race_calendar(year: int) -> list[str]:
    """
    Получение календаря гонок за выбранный год.
    Возвращает список страниц для пагинации.
    """
    url = f"{API_URL}{year}"

    cache_key = f"{CALENDAR_PREFIX}:{year}"
    response = await get_response_or_cached(url, cache_key)
    if response is None:
        return []

    pages = []
    message = ""

    for round, race in enumerate(response["races"], 1):
        # Форматируем заголовок
        header = await format_race_header(
            round=round,
            city=race["circuit"]["city"],
            country=race["circuit"]["country"],
            circuit_name=race["circuit"]["circuitName"],
        )
        message += f"{header}\n"

        # Сортируем события
        events = await sort_events(race["schedule"])

        # Добавляем события
        for event, dt, is_small in events:
            line = format_event_line(
                event=event,
                dt=dt,
                is_small=is_small,
                laps=race.get("laps"),
            )
            message += f"{line}\n"

        message += "\n"
        # Каждые 6 гонок - новая страница
        if round % 8 == 0:
            pages.append(message)
            message = ""
    if message:
        pages.append(message)
    return pages


__all__ = ["get_race_calendar", "get_current_race"]
