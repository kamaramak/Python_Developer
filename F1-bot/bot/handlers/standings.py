from datetime import datetime as dt

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.core.callbacks import (
    BaseCallbackFactory,
    ConstructorsCallbackFactory,
    DriversCallbackFactory,
)
from bot.core.callbacks.base import parse_callback
from bot.core.constants import (
    CONSTRUCTORS_CONTENT_NAME,
    CONSTRUCTORS_PREFIX,
    DRIVERS_CONTENT_NAME,
    DRIVERS_PREFIX,
    STANDINGS_PREFIX,
    UTC,
)
from bot.handlers.base import BaseYearSelectorHandler
from bot.keyboards import (
    get_back_keyboard,
    get_pagination_pages_keyboard,
    get_years_keyboard,
    standings_menu_keyboard,
)
from bot.services.f1_data import F1DataService


class StandingsHandler:
    """Обработчик пилотов"""

    def __init__(self, f1_service: F1DataService):
        super().__init__()
        self.f1_service = f1_service
        self.router = Router()
        self.standings_callbacks = BaseCallbackFactory(self.standings_prefix)
        self.drivers_callbacks = DriversCallbackFactory(self.drivers_prefix)
        self.constructors_callbacks = ConstructorsCallbackFactory(
            self.constructors_prefix
        )
        self._register_standings_handlers()

    def _register_standings_handlers(self):
        """Регистрируем обработчики таблиц."""

        # --- ГЛАВНОЕ МЕНЮ ТАБЛИЦ (REPLY-КНОПКА) ---
        @self.router.message(F.text == "📊 Таблицы")
        async def standings_menu_reply(message: Message, state: FSMContext):
            """Показать меню выбора таблиц результатов."""
            await state.clear()
            await message.answer(
                "📊 Выберите необходимую таблицу:",
                reply_markup=standings_menu_keyboard(
                    drivers_prefix=self.drivers_prefix,
                    constructors_prefix=self.constructors_prefix,
                ),
            )

        # --- ГЛАВНОЕ МЕНЮ ТАБЛИЦ (INLINE-КНОПКА) ---
        @self.router.callback_query(
            lambda c: c.data
            in (
                self.standings_callbacks.callback_back_to_menu(),
                self.drivers_callbacks.callback_back_to_menu(),
                self.constructors_callbacks.callback_back_to_menu(),
            )
        )
        async def standings_menu_inline(
            callback: CallbackQuery, state: FSMContext
        ):
            await state.clear()
            await callback.message.edit_text(
                "📊 Выберите необходимую таблицу:",
                reply_markup=standings_menu_keyboard(
                    drivers_prefix=self.drivers_prefix,
                    constructors_prefix=self.constructors_prefix,
                ),
            )
            await callback.answer()
            return

    @property
    def standings_prefix(self):
        return STANDINGS_PREFIX

    @property
    def drivers_prefix(self):
        return DRIVERS_PREFIX

    @property
    def constructors_prefix(self):
        return CONSTRUCTORS_PREFIX


class DriversStandingsHandler(BaseYearSelectorHandler):
    """Обработчик пилотов"""

    def __init__(self, f1_service: F1DataService):
        super().__init__()
        self.f1_service = f1_service
        self.drivers_callbacks = DriversCallbackFactory(self.section_prefix)
        self._register_drivers_handlers()

    def _register_drivers_handlers(self):
        """Регистрируем обработчики таблиц."""

        # --- ПИЛОТЫ - ВЫБОР СЕЗОНА ИЗ СПИСКА ЛЕТ ---
        @self.router.callback_query(
            lambda c: c.data.startswith(
                self.drivers_callbacks.base_callback_all_years()
            )
        )
        async def drivers_all_years(
            callback: CallbackQuery, state: FSMContext
        ):
            parsed = parse_callback(callback.data)
            decade = int(parsed.value) - (int(parsed.value) % 10)
            await state.clear()
            years = await self.f1_service.get_available_years(decade)
            await callback.message.edit_text(
                "📅 Выберите год:",
                reply_markup=get_years_keyboard(
                    years, self.section_prefix, decade
                ),
            )
            await callback.answer()
            return

    # Абстрактные методы
    @property
    def section_prefix(self):
        return DRIVERS_PREFIX

    @property
    def content_name(self) -> str:
        return DRIVERS_CONTENT_NAME

    async def get_data_for_year(self, year: int, value_type) -> list[str]:
        """Получить календарь за год для пилотов"""
        return await self.f1_service.get_drivers_standings_for_year(year)

    def get_back_keyboard(self):
        return get_back_keyboard(self.section_prefix)

    def get_pagination_keyboard(
        self,
        current_page: int,
        total_pages: int,
    ):
        decade = dt.now(UTC).year - (dt.now(UTC).year % 10)
        return get_pagination_pages_keyboard(
            current_page,
            total_pages,
            self.section_prefix,
            self.drivers_callbacks.callback_all_years(decade),
            self.drivers_callbacks.callback_back_to_menu(),
        )


class ConstructorsStandingsHandler(BaseYearSelectorHandler):
    """Обработчик конструкторов"""

    def __init__(self, f1_service: F1DataService):
        super().__init__()
        self.f1_service = f1_service
        self.constructors_callback = ConstructorsCallbackFactory(
            self.section_prefix
        )
        self._register_constructors_handlers()

    def _register_constructors_handlers(self):
        """Регистрируем обработчики конструкторов."""

        # --- КОНСТРУКТОРЫ - ВЫБОР СЕЗОНА ИЗ СПИСКА ЛЕТ ---
        @self.router.callback_query(
            lambda c: c.data.startswith(
                self.constructors_callback.base_callback_all_years()
            )
        )
        async def constructors_all_years(
            callback: CallbackQuery, state: FSMContext
        ):
            parsed = parse_callback(callback.data)
            decade = int(parsed.value) - (int(parsed.value) % 10)
            await state.clear()
            years = await self.f1_service.get_available_years(decade)
            await callback.message.edit_text(
                "📅 Выберите год:",
                reply_markup=get_years_keyboard(
                    years, self.section_prefix, decade
                ),
            )
            await callback.answer()
            return

    # Абстрактные методы
    @property
    def section_prefix(self):
        return CONSTRUCTORS_PREFIX

    @property
    def content_name(self) -> str:
        return CONSTRUCTORS_CONTENT_NAME

    async def get_data_for_year(self, year: int, value_type) -> list[str]:
        """Получить календарь за год для конструкторов"""
        return await self.f1_service.get_constructors_standings_for_year(year)

    def get_back_keyboard(self):
        return get_back_keyboard(self.section_prefix)

    def get_pagination_keyboard(
        self,
        current_page: int,
        total_pages: int,
    ):
        decade = dt.now(UTC).year - (dt.now(UTC).year % 10)
        return get_pagination_pages_keyboard(
            current_page,
            total_pages,
            self.section_prefix,
            self.constructors_callback.callback_all_years(decade),
            self.constructors_callback.callback_back_to_menu(),
        )


def setup(router, f1_service: F1DataService):
    """Фабрика для создания обработчика с зависимостями"""
    standings_handler = StandingsHandler(f1_service)
    drivers_handler = DriversStandingsHandler(f1_service)
    constructors_handler = ConstructorsStandingsHandler(f1_service)
    router.include_router(standings_handler.router)
    router.include_router(drivers_handler.router)
    router.include_router(constructors_handler.router)
