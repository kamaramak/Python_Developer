"""Основной сервис для работы с F1 данными"""

from datetime import datetime

from bot.core.constants import (
    FP1_ID,
    FP2_ID,
    FP3_ID,
    QUALY_ID,
    RACE_ID,
    SPRINT_QUALY_ID,
    SPRINT_RACE_ID,
    UTC,
)
from bot.keyboards.results import get_results_round_keyboard

from .calendar import get_current_race, get_race_calendar
from .results import (
    get_current_results_fp,
    get_current_results_qualy,
    get_current_results_race,
    get_results_race_for_year,
    get_text_for_current_results_menu,
)
from .standings import (
    get_constructors_standings_for_year,
    get_drivers_standings_for_year,
)


class F1DataService:
    """
    Единый интерфейс для всех F1 данных.
    Хендлеры работают ТОЛЬКО через этот класс!
    """

    # --- COMMON YEARS
    async def get_available_years(self, decade) -> list[int]:
        """
        Получить доступные годы.
        Пока статический список, потом можно сделать динамическим
        """
        current_year = datetime.now(UTC).year
        return range(decade, min(decade + 10, current_year + 1))

    # --- CALENDAR ---
    async def get_current_race(self) -> str:
        """Получить ближайшую гонку"""
        return await get_current_race()

    async def get_race_calendar(self, year: int) -> list[str]:
        """Получить календарь гонок"""
        return await get_race_calendar(year)

    # --- STANDINGS ---
    async def get_drivers_standings_for_year(self, year: int) -> list[str]:
        """Получить личный зачет пилотов"""
        return await get_drivers_standings_for_year(year)

    async def get_constructors_standings_for_year(
        self, year: int
    ) -> list[str]:
        """Получить кубок конструкторов"""
        return await get_constructors_standings_for_year(year)

    # --- RESULTS OF FP 1-3 ---
    async def get_current_results(self, year, value_type) -> list[str]:
        """Получить результаты текущего заезда по идентификатору заезда."""
        if year < 0:
            if value_type in (FP1_ID, FP2_ID, FP3_ID):
                return await get_current_results_fp(value_type)
            if value_type in (SPRINT_QUALY_ID, QUALY_ID):
                return await get_current_results_qualy(value_type)
            if value_type in (RACE_ID, SPRINT_RACE_ID):
                return await get_current_results_race(value_type)
        else:
            return await get_results_race_for_year(value_type, year)

    async def get_text_for_current_results_menu(self):
        return await get_text_for_current_results_menu()

    async def get_results_round_keyboard(self, section_prefix, year):
        return await get_results_round_keyboard(section_prefix, year)


__all__ = ["F1DataService"]
