from typing import Optional

from bot.core.constants import (
    API_URL,
    EVENTS_FOR_REMAINING_TIME,
    EVENTS_FOR_RESULTS,
    NO_DATA_ERROR,
    RACE_ID,
    RESULTS_PREFIX,
)

from .base import get_response_or_cached
from .formatters.results import (
    format_fp_gap,
    format_qualy_gap,
    format_race_gap,
    format_results_body,
    format_results_header,
    format_text_for_results_menu,
    sort_fp_results,
    sort_qualy_results,
    sort_race_results,
)


async def get_text_for_current_results_menu():
    url = f"{API_URL}current/last/{RACE_ID}"
    cache_key = f"{RESULTS_PREFIX}:current:{RACE_ID}"
    response = await get_response_or_cached(url=url, cache_key=cache_key)
    if response is None:
        return NO_DATA_ERROR
    race_info = response["races"]
    round = race_info["round"]
    city = race_info["circuit"]["city"]
    country = race_info["circuit"]["country"]
    circuit_name = race_info["circuit"]["circuitName"]
    text = await format_text_for_results_menu(
        round=round,
        city=city,
        country=country,
        circuit_name=circuit_name,
    )
    text += (
        "🏆Выберите необходимый заезд для просмотра результатов (спринт-заезды "
        "обозначены символом ⚡)\n"
        "P.S. Результаты текущих заездов доступны только после завершения "
        "текущего гоночного уик-енда, данные обновляются каждые 10 минут."
    )
    return text


async def get_results_header(
    race_id: str, race_info: dict, is_current: Optional[bool] = False
):
    if is_current:
        header = (
            f"<b>{EVENTS_FOR_RESULTS[race_id][0]} Результаты крайней "
            f"{EVENTS_FOR_REMAINING_TIME[race_id]}:\n</b>"
        ).upper()
    else:
        header = (
            f"<b>{EVENTS_FOR_RESULTS[race_id][0]} Результаты "
            f"{EVENTS_FOR_REMAINING_TIME[race_id]}:\n</b>"
        ).upper()

    if "date" in race_info:
        race_date = race_info["date"]
    else:
        race_date = race_info[f"{race_id}Date"]

    if "time" in race_info:
        race_time = race_info["time"]
    else:
        race_time = race_info[f"{race_id}Time"]

    if ":" in race_date:
        race_date, race_time = race_time, race_date

    round = race_info["round"]
    city = race_info["circuit"]["city"]
    country = race_info["circuit"]["country"]
    circuit_name = race_info["circuit"]["circuitName"]
    header += await format_results_header(
        round=round,
        race_date=race_date,
        race_time=race_time,
        city=city,
        country=country,
        circuit_name=circuit_name,
    )
    return header


async def get_results_body(
    race_id: str,
    position: int,
    prev_time: str,
    result: dict,
    driver_time: Optional[str] = None,
    qualy_sessions: Optional[str] = None,
):
    body = ""
    driver = result["driver"]
    team = result["team"]
    if driver_time is None:
        driver_time = result["time"]
    name = driver["name"]
    surname = driver["surname"]
    country = driver["nationality"]
    number = driver["number"]
    shortname = driver["shortName"]
    team_name = team["teamName"]
    team_wiki_id = team["url"].split("/wiki/")[-1]
    body += await format_results_body(
        position=position,
        driver_time=driver_time,
        name=name,
        surname=surname,
        country=country,
        number=number,
        shortname=shortname,
        team_name=team_name,
        team_wiki_id=team_wiki_id,
        qualy_sessions=qualy_sessions,
    )

    if prev_time is not None:
        if "fp" in race_id.lower():
            body += await format_fp_gap(
                prev=prev_time,
                driver_time=driver_time,
                position=position,
            )
        elif "qualy" in race_id.lower():
            body += await format_qualy_gap(
                prev_times=prev_time,
                driver_times=driver_time,
                qualy_sessions=qualy_sessions,
                position=position,
            )
        else:
            body += await format_race_gap(
                driver_time=driver_time,
            )
    return body


async def get_current_results_fp(race_id: str):
    """
    Получение результатов крайних свободных практик.
    Возвращает список страниц для пагинации.
    """
    url = f"{API_URL}current/last/{race_id}"
    cache_key = f"{RESULTS_PREFIX}:current:{race_id}"
    response = await get_response_or_cached(url=url, cache_key=cache_key)
    if response is None:
        return []
    race_info = response["races"]
    pages = []
    message = ""
    header = await get_results_header(race_id, race_info)
    message += header

    results: list[dict] = await sort_fp_results(race_info[f"{race_id}Results"])
    position = 1
    prev_time = None
    for result in results:
        if not message:
            message += header
        message += await get_results_body(
            race_id=race_id,
            position=position,
            prev_time=prev_time,
            result=result,
        )
        prev_time = result["time"]
        message += "\n"
        if position % 4 == 0:
            pages.append(message)
            message = ""
        position += 1
    if message:
        pages.append(message)
    return pages


async def get_current_results_qualy(race_id: str):
    """
    Получение результатов крайней квалификации.
    Возвращает список страниц для пагинации
    """
    path = "sprint/qualy" if "sprint" in race_id else race_id
    url = f"{API_URL}current/last/{path}"
    cache_key = f"{RESULTS_PREFIX}:current:{race_id}"
    response = await get_response_or_cached(url=url, cache_key=cache_key)
    if response is None:
        return []
    race_info = response["races"]
    pages = []
    message = ""
    header = await get_results_header(race_id, race_info)
    message += header

    results: list[dict] = await sort_qualy_results(
        race_info[f"{race_id}Results"]
    )
    prev_time = None
    for result in results:
        if not message:
            message += header

        if "sprint" in race_id:
            driver_time = (result["sq1"], result["sq2"], result["sq3"])
            qualy_sessions = ("sq1", "sq2", "sq3")
        else:
            driver_time = (result["q1"], result["q2"], result["q3"])
            qualy_sessions = ("q1", "q2", "q3")

        position = result["gridPosition"]
        message += await get_results_body(
            race_id=race_id,
            position=position,
            prev_time=prev_time,
            result=result,
            driver_time=driver_time,
            qualy_sessions=qualy_sessions,
        )
        prev_time = driver_time
        message += "\n"
        if position % 4 == 0:
            pages.append(message)
            message = ""
    if message:
        pages.append(message)
    return pages


async def get_current_results_race(race_id: str):
    """
    Получение результатов крайней гонки.
    Возвращает список страниц для пагинации
    """
    path = "sprint/race" if "sprint" in race_id else race_id
    url = f"{API_URL}current/last/{path}"
    cache_key = f"{RESULTS_PREFIX}:current:{race_id}"

    response = await get_response_or_cached(url=url, cache_key=cache_key)
    if response is None:
        return []
    race_info = response["races"]
    pages = []
    message = ""

    header = await get_results_header(race_id, race_info)
    message += header

    results_key = "results" if "results" in race_info else f"{race_id}Results"
    results: list[dict] = await sort_race_results(race_info[results_key])
    prev_time = None
    position = 1
    for result in results:
        if not message:
            message += header

        driver_time = result["time"] if "time" in result else "-"
        message += await get_results_body(
            race_id=race_id,
            position=position,
            prev_time=prev_time,
            result=result,
            driver_time=driver_time,
        )
        prev_time = driver_time
        message += "\n"
        if position % 4 == 0:
            pages.append(message)
            message = ""
        position += 1
    if message:
        pages.append(message)
    return pages


async def get_results_race_for_year(round: int, year: int):
    """
    Получение результатов гонки за конкретный год.
    Возвращает список страниц для пагинации
    """
    race_id = RACE_ID
    url = f"{API_URL}{year}/{round}/{race_id}"
    cache_key = f"{RESULTS_PREFIX}:{year}:{round}"

    response = await get_response_or_cached(url=url, cache_key=cache_key)
    if response is None:
        return []
    race_info = response["races"]
    pages = []
    message = ""

    header = await get_results_header(race_id, race_info)
    message += header

    results: list[dict] = await sort_race_results(race_info["results"])
    prev_time = None
    count = 1
    for result in results:
        if not message:
            message += header

        position = result["position"]
        driver_time = result["time"] if "time" in result else "-"
        message += await get_results_body(
            race_id=race_id,
            position=position,
            prev_time=prev_time,
            result=result,
            driver_time=driver_time,
        )
        prev_time = driver_time
        message += "\n"
        if count % 4 == 0:
            pages.append(message)
            message = ""
        count += 1
    if message:
        pages.append(message)
    return pages
