from datetime import datetime as dt

import emoji
from dateutil import relativedelta

from bot.core.constants import (
    COUNTRIES,
    EMOJI_FLAGS,
    EMOJI_TEAMS,
    HARD_NAMES,
    NATIONALITY_TO_COUNTRY,
    UTC,
)

from .base import format_russian_text
from .translator import translate


async def format_driver_header(
    points: int,
    position: int,
    wins: int,
    name: str,
    surname: str,
    driver_country: str,
    birthday: str,
    number: int,
    short_name: str,
    team_name: str,
    team_wiki_id: str,
) -> str:
    fullname = f"{name} {surname}".upper()
    if fullname in HARD_NAMES:
        fullname_ru = HARD_NAMES[fullname]
    else:
        fullname_ru = await translate(fullname)
    driver_country_ru = await translate(driver_country)
    driver_country_ru = COUNTRIES.get(driver_country_ru, driver_country_ru)
    driver_country_ru = NATIONALITY_TO_COUNTRY.get(
        driver_country_ru.lower(), driver_country_ru
    )
    if driver_country_ru in EMOJI_FLAGS:
        nationality_flag = emoji.emojize(
            f"{EMOJI_FLAGS[driver_country_ru]}", language="alias"
        )
    else:
        nationality_flag = ""

    if "-" in birthday:
        format = "%Y-%m-%d"
    else:
        format = "%d/%m/%Y"

    birthday_date = dt.strptime(birthday, format).replace(tzinfo=UTC)
    today = dt.now(UTC)
    age = relativedelta.relativedelta(today, birthday_date).years
    birthday_ru = dt.strftime(birthday_date, "%d.%m.%Y")

    age_text = format_russian_text(age, "год", "года", "лет")
    points_text = format_russian_text(points, "очко", "очка", "очков")
    wins_text = format_russian_text(wins, "победа", "победы", "побед")

    cup = ""
    if position == 1:
        cup = "🏆 "
    team_emoji = EMOJI_TEAMS[team_wiki_id]

    return (
        f"<b>{cup}{position}. {fullname_ru} (#{number} {short_name})</b>\n"
        f"{nationality_flag} {driver_country_ru} | {birthday_ru} "
        f"({age} {age_text})\n"
        f"{team_emoji} {team_name}\n"
        f"{points} {points_text} · {wins} {wins_text}\n"
    )


async def format_driver_gap(
    prev: int,
    points: int,
    position: int,
) -> str:
    gap = prev - points
    gap_text = format_russian_text(gap, "очко", "очка", "очков")
    swords = ""
    if gap < 25:
        swords = "⚔️"

    return (
        f"{'-' * 15}\n"
        f"🔻-{gap} {gap_text} отставания от P{position - 1}{swords}\n"
    )


async def format_constructor_header(
    points: int,
    position: str,
    wins: int,
    team_name: str,
    team_country: str,
    since: int,
    team_cup_wins: int,
    driver_wins: int,
    team_wiki_id: str,
) -> str:
    fullname = team_name.upper()
    team_country_ru = await translate(team_country)
    team_country_ru = COUNTRIES.get(team_country_ru, team_country_ru)
    team_country_ru = NATIONALITY_TO_COUNTRY.get(
        team_country_ru.lower(), team_country_ru
    )
    if team_country_ru in EMOJI_FLAGS:
        team_country_flag = emoji.emojize(
            f"{EMOJI_FLAGS[team_country_ru]}", language="alias"
        )
    else:
        team_country_flag = ""

    since_block = ""
    if since:
        format = "%Y"
        since_date = dt.strptime(str(since), format).replace(tzinfo=UTC)
        today = dt.now(UTC)
        age = relativedelta.relativedelta(today, since_date).years
        since_date_text = dt.strftime(since_date, "%Y")
        age_text = format_russian_text(age, "год", "года", "лет")
        since_block += f"| est. {since_date_text} ({age} {age_text})"

    points_text = format_russian_text(points, "очко", "очка", "очков")
    wins_text = format_russian_text(wins, "победа", "победы", "побед")

    cup = ""
    if position == 1:
        cup = "🏆 "
    team_emoji = EMOJI_TEAMS[team_wiki_id]
    header = (
        f"<b>{cup}{team_emoji} {position}. {fullname}</b>\n"
        f"{team_country_flag} {team_country_ru} {since_block}\n"
        f"{points} {points_text} · {wins} {wins_text}"
    )
    wins_text = "\nТитулы: "
    if team_cup_wins:
        team_cup_wins_text = f"{team_cup_wins} конструкторских"
    else:
        team_cup_wins_text = ""
    if driver_wins:
        driver_wins_text = f"{driver_wins} личных."
    else:
        driver_wins_text = ""
    team_wins = (team_cup_wins_text, driver_wins_text)
    if any(team_wins):
        wins_text += f"{', '.join(team_wins)}\n"
    else:
        wins_text += "\n"
    header += wins_text
    return header


async def format_constructor_gap(
    prev: int,
    points: int,
    position: int,
) -> str:
    gap = prev - points
    gap_text = format_russian_text(gap, "очко", "очка", "очков")
    swords = ""
    if gap < 43:
        swords = "⚔️"

    return (
        f"{'-' * 15}\n"
        f"🔻-{gap} {gap_text} отставания от P{position - 1}{swords}\n"
    )
