"""Сервис для работы с турнирными таблицами"""

from bot.core.constants import (
    API_URL,
    CONSTRUCTORS_PREFIX,
    DRIVERS_PREFIX,
)

from .base import get_response_or_cached
from .formatters.standings import (
    format_constructor_gap,
    format_constructor_header,
    format_driver_gap,
    format_driver_header,
)


async def get_drivers_standings_for_year(year: int) -> list[str]:
    """
    Получение личного зачета пилотов.
    возвращает список страниц для пагинации.
    """
    url = f"{API_URL}{year}/drivers-championship/"

    cache_key = f"{DRIVERS_PREFIX}:{year}"
    response = await get_response_or_cached(url, cache_key)
    if response is None:
        return []

    pages = []
    message = ""
    common_header = f"<b>СЕЗОН {year}\nЛИЧНЫЙ ЗАЧЁТ</b>\n\n"
    message += common_header
    prev_points = None
    for driver in response["drivers_championship"]:
        if not message:
            message += common_header
        position = int(driver["position"])
        points = int(driver["points"])
        wins = int(driver["wins"])
        name = driver["driver"]["name"]
        surname = driver["driver"]["surname"]
        driver_country = driver["driver"]["nationality"]
        birthday = driver["driver"]["birthday"]
        number_raw = driver["driver"]["number"]
        number = int(number_raw) if number_raw else ""
        short_name = driver["driver"]["shortName"] or ""
        team_name = driver["team"]["teamName"]
        team_wiki_id = driver["team"]["url"].split("/wiki/")[-1]

        header = await format_driver_header(
            points=points,
            position=position,
            wins=wins,
            name=name,
            surname=surname,
            driver_country=driver_country,
            birthday=birthday,
            number=number,
            short_name=short_name,
            team_name=team_name,
            team_wiki_id=team_wiki_id,
        )
        message += header

        if prev_points is not None:
            driver_gap = await format_driver_gap(
                prev=prev_points,
                points=points,
                position=position,
            )
            message += driver_gap
        prev_points = points
        message += "\n"
        if position % 4 == 0:
            pages.append(message)
            message = ""
    if message:
        pages.append(message)
    return pages


async def get_constructors_standings_for_year(year: int) -> list[str]:
    """
    Получение кубка конструкторов.
    """
    url = f"{API_URL}{year}/constructors-championship/"

    cache_key = f"{CONSTRUCTORS_PREFIX}:{year}"
    response = await get_response_or_cached(url, cache_key)
    if response is None:
        return []

    pages = []
    message = ""
    common_header = f"<b>СЕЗОН {year}\nКУБОК КОНСТРУКТОРОВ</b>\n\n"
    message += common_header
    prev_points = None
    for team in response["constructors_championship"]:
        if not message:
            message += common_header
        position = int(team["position"])
        points = int(team["points"])
        wins = int(team["wins"])
        team_name = team["team"]["teamName"]
        team_country = team["team"]["country"]
        since_raw = team["team"]["firstAppareance"]
        since = int(since_raw) if since_raw else ""
        team_cup_wins_raw = team["team"]["constructorsChampionships"]
        team_cup_wins = int(team_cup_wins_raw) if team_cup_wins_raw else ""
        driver_wins_raw = team["team"]["driversChampionships"]
        driver_wins = int(driver_wins_raw) if driver_wins_raw else ""
        team_wiki_id = team["team"]["url"].split("/wiki/")[-1]

        header = await format_constructor_header(
            points=points,
            position=position,
            wins=wins,
            team_name=team_name,
            team_country=team_country,
            since=since,
            team_cup_wins=team_cup_wins,
            driver_wins=driver_wins,
            team_wiki_id=team_wiki_id,
        )
        message += header

        if prev_points is not None:
            constructor_gap = await format_constructor_gap(
                prev=prev_points,
                points=points,
                position=position,
            )
            message += constructor_gap
        prev_points = points
        message += "\n"
        if position % 4 == 0:
            pages.append(message)
            message = ""
    if message:
        pages.append(message)
    return pages


__all__ = [
    "get_drivers_standings_for_year",
    "get_constructors_standings_for_year",
]
