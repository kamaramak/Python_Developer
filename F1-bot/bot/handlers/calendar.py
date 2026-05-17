from datetime import datetime as dt

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.core.callbacks import CalendarCallbackFactory
from bot.core.callbacks.base import parse_callback
from bot.core.constants import CALENDAR_CONTENT_NAME, CALENDAR_PREFIX, UTC
from bot.handlers.base import BaseYearSelectorHandler
from bot.keyboards import (
    calendar_current_race_keyboard,
    calendar_menu_keyboard,
    get_back_keyboard,
    get_pagination_pages_keyboard,
    get_years_keyboard,
)
from bot.services.f1_data import F1DataService


class CalendarHandler(BaseYearSelectorHandler):
    """Обработчик календаря гонок"""

    def __init__(self, f1_service: F1DataService):
        super().__init__()
        self.f1_service = f1_service
        self.calendar_callbacks = CalendarCallbackFactory(self.section_prefix)
        self._register_calendar_handlers()

    def _register_calendar_handlers(self):
        """Регистрируем обработчики календаря"""

        # --- ГЛАВНОЕ МЕНЮ КАЛЕНДАРЯ (REPLY-КНОПКА) ---
        @self.router.message(F.text == "🗓 Календарь")
        async def calendar_menu_reply(message: Message, state: FSMContext):
            await state.clear()
            await message.answer(
                "🗓 Выберите необходимый календарь:",
                reply_markup=calendar_menu_keyboard(self.section_prefix),
            )

        # --- ГЛАВНОЕ МЕНЮ КАЛЕНДАРЯ (INLINE-КНОПКА) ---
        @self.router.callback_query(
            lambda c: c.data == self.calendar_callbacks.callback_back_to_menu()
        )
        async def calendar_menu_inline(
            callback: CallbackQuery, state: FSMContext
        ):
            await state.clear()
            await callback.message.edit_text(
                "🗓 Выберите необходимый календарь:",
                reply_markup=calendar_menu_keyboard(self.section_prefix),
            )
            await callback.answer()
            return

        # --- ВЫБОР СЕЗОНА ИЗ СПИСКА ЛЕТ ---
        @self.router.callback_query(
            lambda c: c.data.startswith(
                self.calendar_callbacks.base_callback_all_years()
            )
        )
        async def calendar_all_years(
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

        # --- БЛИЖАЙШАЯ ГОНКА (REPLY-КНОПКА) ---
        @self.router.message(F.text == "⏭️ Ближайший Гран-При")
        async def calendar_current_race_reply(
            message: Message, state: FSMContext
        ):
            await state.clear()
            await message.answer(
                await self.f1_service.get_current_race(),
                parse_mode="HTML",
                reply_markup=calendar_current_race_keyboard(
                    self.section_prefix
                ),
            )

        # --- БЛИЖАЙШАЯ ГОНКА (INLINE-КНОПКА) ---
        @self.router.callback_query(
            lambda c: c.data == self.calendar_callbacks.calendar_current_race()
        )
        async def calendar_current_race_inline(
            callback: CallbackQuery,
            state: FSMContext,
        ):
            await state.clear()
            await callback.message.edit_text(
                await self.f1_service.get_current_race(),
                parse_mode="HTML",
                reply_markup=calendar_current_race_keyboard(
                    self.section_prefix
                ),
            )

    # Абстрактные методы
    @property
    def section_prefix(self) -> str:
        return CALENDAR_PREFIX

    @property
    def content_name(self) -> str:
        return CALENDAR_CONTENT_NAME

    async def get_data_for_year(self, year: int, value_type) -> list[str]:
        """Получить календарь за год"""
        return await self.f1_service.get_race_calendar(year)

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
            self.calendar_callbacks.callback_all_years(decade),
            self.calendar_callbacks.callback_back_to_menu(),
        )


def setup(router, f1_service: F1DataService):
    """Фабрика для создания обработчика с зависимостями"""
    handler = CalendarHandler(f1_service)
    router.include_router(handler.router)
