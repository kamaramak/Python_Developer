"""Собираем все клавиатуры в одном месте для удобного импорта"""

# Reply-клавиатуры
from .calendar import calendar_current_race_keyboard, calendar_menu_keyboard
from .common import (
    get_back_keyboard,
)
from .main_menu import menu_keyboard
from .pagination import (
    get_pagination_numbers_keyboard,
    get_pagination_pages_keyboard,
)
from .results import results_menu_keyboard
from .standings import standings_menu_keyboard
from .year_selector import get_years_keyboard

# Экспортируем ВСЁ, что нужно в хендлерах
__all__ = [
    # Menu
    "menu_keyboard",
    # Calendar
    "calendar_menu_keyboard",
    "calendar_current_race_keyboard",
    # Standings
    "standings_menu_keyboard",
    # Results
    "results_menu_keyboard",
    # Pagination
    "get_pagination_pages_keyboard",
    "get_pagination_numbers_keyboard",
    # Year selector
    "get_years_keyboard",
    # Common
    "get_back_keyboard",
]
