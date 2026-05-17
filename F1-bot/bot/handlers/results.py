from datetime import datetime as dt

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.core.callbacks import ResultsCallbackFactory
from bot.core.callbacks.base import parse_callback
from bot.core.constants import (
    RACE_ID,
    RESULTS_CONTENT_NAME,
    RESULTS_PREFIX,
    UTC,
)
from bot.core.pagination import PaginationState
from bot.handlers.base import BaseYearSelectorHandler
from bot.keyboards import (
    get_back_keyboard,
    get_pagination_pages_keyboard,
    get_years_keyboard,
    results_menu_keyboard,
)
from bot.services.f1_data import F1DataService


class ResultsHandler(BaseYearSelectorHandler):
    """Обработчик просмотра результатов заездов."""

    def __init__(self, f1_service: F1DataService):
        super().__init__()
        self.f1_service = f1_service
        self.results_callbacks = ResultsCallbackFactory(self.section_prefix)
        self._register_results_handler()
        self.value_type = None

    def _register_results_handler(self):
        """Регистрируем обработчики результатов."""

        # --- ГЛАВНОЕ МЕНЮ РЕЗУЛЬТАТОВ (REPLY-КНОПКА) ---
        @self.router.message(F.text == "🏆 Результаты")
        async def results_menu_reply(message: Message, state: FSMContext):
            await state.clear()
            await message.answer(
                await self.get_text_for_current_results_menu(),
                parse_mode="HTML",
                reply_markup=results_menu_keyboard(self.section_prefix),
            )

        # --- ГЛАВНОЕ МЕНЮ РЕЗУЛЬТАТОВ (INLINE-КНОПКА) ---
        @self.router.callback_query(
            lambda c: c.data == self.results_callbacks.callback_back_to_menu()
        )
        async def results_menu_inline(
            callback: CallbackQuery, state: FSMContext
        ):
            await state.clear()
            await callback.message.edit_text(
                await self.get_text_for_current_results_menu(),
                parse_mode="HTML",
                reply_markup=results_menu_keyboard(self.section_prefix),
            )
            await callback.answer()
            return

        # --- РЕЗУЛЬТАТЫ - ВЫБОР СЕЗОНА ИЗ СПИСКА ЛЕТ ---
        @self.router.callback_query(
            lambda c: c.data.startswith(
                self.results_callbacks.base_callback_all_years()
            )
        )
        async def results_all_years(
            callback: CallbackQuery, state: FSMContext
        ):
            await state.clear()
            parsed = parse_callback(callback.data)
            decade = int(parsed.value) - (int(parsed.value) % 10)
            years = await self.f1_service.get_available_years(decade)
            await callback.message.edit_text(
                "📅 Выберите год:",
                reply_markup=get_years_keyboard(
                    years, self.section_prefix, decade, value_type="special"
                ),
            )
            await callback.answer()
            return

        # --- ВЫДАЧА ВСЕХ ЭТАПОВ ВЫБРАННОГО СЕЗОНА ДЛЯ РЕЗУЛЬТАТОВ ---
        @self.router.callback_query(lambda c: "special" in c.data)
        async def results_all_rounds_of_year(
            callback: CallbackQuery, state: FSMContext
        ):
            await state.clear()
            parsed = parse_callback(callback.data)
            year = int(parsed.value)

            await callback.message.edit_text(
                f"Выберите этап сезона {year}",
                parse_mode="HTML",
                reply_markup=await self.get_results_round_keyboard(
                    self.section_prefix, year
                ),
            )
            await callback.answer()

        # --- РЕЗУЛЬТАТЫ КРАЙНЕЙ ГОНКИ (REPLY-КНОПКА) ---
        @self.router.message(F.text == "🏁 Результаты крайней гонки")
        async def results_current_race(message: Message, state: FSMContext):
            await state.clear()
            pages = await self.get_data_for_year(-1, RACE_ID)

            if not pages:
                await message.answer(
                    "❌ Запрашиваемые данные отсутствюуют.",
                    reply_markup=self.get_back_keyboard(),
                )

            await state.set_state(PaginationState.viewing)
            await state.update_data(pages=pages, current_page=0)

            await message.answer(
                pages[0],
                parse_mode="HTML",
                reply_markup=self.get_pagination_keyboard(
                    0,
                    len(pages),
                ),
            )

    # Абстрактные методы
    @property
    def section_prefix(self) -> str:
        return RESULTS_PREFIX

    @property
    def content_name(self) -> str:
        return RESULTS_CONTENT_NAME

    async def get_data_for_year(self, year, value_type) -> list[str]:
        """Получить результаты за год"""
        return await self.f1_service.get_current_results(year, value_type)

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
            self.results_callbacks.callback_all_years(decade),
            self.results_callbacks.callback_back_to_menu(),
        )

    async def get_text_for_current_results_menu(self):
        return await self.f1_service.get_text_for_current_results_menu()

    async def get_results_round_keyboard(self, section_prefix, year):
        return await self.f1_service.get_results_round_keyboard(
            section_prefix, year
        )


def setup(router, f1_service: F1DataService):
    """Фабрика для создания обработчика с зависимостями"""
    handler = ResultsHandler(f1_service)
    router.include_router(handler.router)
