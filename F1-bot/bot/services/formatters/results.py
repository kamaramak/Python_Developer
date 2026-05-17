from datetime import datetime as dt
from datetime import timedelta as td
from typing import Optional

import emoji

from bot.core.constants import (
    COUNTRIES,
    DATETIME_FORMAT_SMALL_INP,
    DATETIME_FORMAT_SMALL_OUT,
    EMOJI_FLAGS,
    EMOJI_TEAMS,
    HARD_NAMES,
    NATIONALITY_TO_COUNTRY,
    RACE_TIME,
    TIME_FORMAT_INP,
    TIME_FORMAT_OUT,
    UTC,
    UTC_DELTA,
)

from .translator import translate


async def format_results_round_keyboard(
    round: int,
    country: str,
):
    country_ru = await translate(country)
    country_ru = COUNTRIES.get(country_ru, country_ru)
    country_ru = NATIONALITY_TO_COUNTRY.get(country_ru.lower(), country_ru)
    country_flag = emoji.emojize(
        f"{EMOJI_FLAGS[country_ru]}", language="alias"
    )
    return f"{country_flag}{round}. {country_ru}"


async def format_text_for_results_menu(
    round: int,
    city: str,
    country: str,
    circuit_name: str,
):
    """Форматирование заголовка меню"""
    city_ru = await translate(city)
    country_ru = await translate(country)
    country_ru = COUNTRIES.get(country_ru, country_ru)
    country_ru = NATIONALITY_TO_COUNTRY.get(country_ru.lower(), country_ru)
    circuit_name_ru = await translate(circuit_name)
    country_flag = emoji.emojize(
        f"{EMOJI_FLAGS[country_ru]}", language="alias"
    )

    header = (
        f"<b>{country_flag}ЭТАП {round}. {city_ru.upper()}, "
        f"{country_ru.upper()}\n"
        f"{circuit_name_ru.upper()}</b>\n"
    )
    return header


async def format_results_header(
    round: int,
    race_date: str,
    race_time: str,
    city: str,
    country: str,
    circuit_name: str,
):
    """Форматирование заголовка этапа"""
    city_ru = await translate(city)
    country_ru = await translate(country)
    country_ru = COUNTRIES.get(country_ru, country_ru)
    country_ru = NATIONALITY_TO_COUNTRY.get(country_ru.lower(), country_ru)
    circuit_name_ru = await translate(circuit_name)
    country_flag = emoji.emojize(
        f"{EMOJI_FLAGS[country_ru]}", language="alias"
    )
    race_date_out = dt.strptime(race_date, DATETIME_FORMAT_SMALL_INP)
    if race_time is not None:
        race_time_out = dt.strptime(race_time, TIME_FORMAT_INP)
        race_time_out.replace(tzinfo=UTC)
        race_time_out += td(hours=UTC_DELTA)
        race_time_text = race_time_out.strftime(TIME_FORMAT_OUT)
    else:
        race_time_text = ""

    header = (
        f"<b>{country_flag}ЭТАП {round}. {city_ru.upper()}, "
        f"{country_ru.upper()}\n"
        f"{circuit_name_ru.upper()}\n"
        f"{race_date_out.strftime(DATETIME_FORMAT_SMALL_OUT)} "
        f"{race_time_text}</b>\n\n"
    )
    return header


async def format_results_body(
    position: int,
    name: str,
    surname: str,
    country: str,
    number: int,
    shortname: str,
    team_name: str,
    team_wiki_id: str,
    driver_time: str,
    qualy_sessions: Optional[str] = None,
):
    if qualy_sessions is not None:
        segments = ""
        for time, segm in zip(driver_time, qualy_sessions):
            if time is None:
                segments += f"⏱️Нет установленного времени в {segm.upper()}\n"
            else:
                segments += f"⏱️{segm.upper()} {time.strip('\\t')}\n"
    elif "+" in driver_time or ":" not in driver_time:
        segments = ""
    else:
        segments = f"⏱️{driver_time}\n"

    number_text = f"#{number}" if number is not None else ""
    shortname_text = shortname or ""

    fullname = f"{name} {surname}".upper()
    if fullname in HARD_NAMES:
        fullname_ru = HARD_NAMES[fullname]
    else:
        fullname_ru = await translate(fullname)
    country_ru = await translate(country)
    country_ru = COUNTRIES.get(country_ru, country_ru)
    country_ru = NATIONALITY_TO_COUNTRY.get(country_ru.lower(), country_ru)
    if country_ru in EMOJI_FLAGS:
        flag = emoji.emojize(f"{EMOJI_FLAGS[country_ru]}", language="alias")
    else:
        flag = ""
    cup = ""
    if position == 1:
        cup = "🏆 "
    team_emoji = EMOJI_TEAMS[team_wiki_id]
    return (
        f"<b>{cup}{flag} {position}. {fullname_ru} "
        f"({number_text} {shortname_text})</b>\n"
        f"{team_emoji} {team_name}\n"
        f"{segments}"
    )


async def format_fp_gap(
    prev: str,
    driver_time: str,
    position: int,
) -> str:
    prev_dt = dt.strptime(prev, RACE_TIME)
    driver_time_dt = dt.strptime(driver_time, RACE_TIME)
    gap_td = driver_time_dt - prev_dt
    total_seconds = gap_td.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60
    gap_formatted = f"🔻+{minutes}:{seconds:06.3f}"

    return f"{'-' * 15}\n" f"{gap_formatted} отставания от P{position - 1}\n"


async def format_qualy_gap(
    prev_times: list,
    driver_times: list,
    qualy_sessions: list,
    position: int,
) -> str:
    driver_time_dt = None
    for prev, time, segm in zip(prev_times, driver_times, qualy_sessions):
        if time is None:
            break
        prev_dt = dt.strptime(prev, RACE_TIME)
        driver_time_dt = dt.strptime(time, RACE_TIME)
        final_driver_segment = segm.upper()
    if driver_time_dt is not None:
        gap_td = driver_time_dt - prev_dt
        total_seconds = gap_td.total_seconds()
        minutes = int(total_seconds // 60)
        seconds = total_seconds % 60
        gap_formatted = f"🔻{final_driver_segment} +{minutes}:{seconds:06.3f}"
    else:
        gap_formatted = "🔻Нет установленного времени в Q3"

    return f"{'-' * 15}\n" f"{gap_formatted} отставания от P{position - 1}\n"


async def format_race_gap(
    driver_time: str,
):
    if driver_time.replace(" ", "").isalpha():
        driver_time_text = "🔻Отсутствует время гонки.\n"
    else:
        driver_time_text = f"🔻{driver_time} отставания от P1\n"
    return f"{'-' * 15}\n{driver_time_text}"


async def sort_fp_results(
    results: list[dict],
):
    sorted_results = sorted(results, key=lambda result: result["time"])
    return sorted_results


async def sort_qualy_results(
    results: list[dict],
):
    sorted_results = sorted(results, key=lambda result: result["gridPosition"])
    return sorted_results


async def sort_race_results(
    results: list[dict],
):
    # Разделить численные позиции от текстовых
    numeric = [r for r in results if str(r["position"]).isdigit()]
    text = [r for r in results if not str(r["position"]).isdigit()]

    # Сортируем числовые
    numeric.sort(key=lambda x: int(x["position"]))

    # Объединение сначала численных, затем текстовых значений
    return numeric + text
