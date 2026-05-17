from abc import ABC, abstractmethod
from typing import Optional

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.core.callbacks import BaseCallbackFactory
from bot.core.callbacks.base import parse_callback
from bot.core.constants import NO_DATA_ERROR
from bot.core.pagination import PaginationState


class BasePaginationHandler(ABC):
    """
    Абстрактный базовый класс для пагинации.
    """

    def __init__(self):
        self.router = Router()
        self.callbacks = BaseCallbackFactory(self.section_prefix)
        self._register_pagination_handler()

    def _register_pagination_handler(self):
        @self.router.callback_query(
            lambda c: c.data.startswith(
                self.callbacks.base_callback_pagination()
            )
        )
        async def handle_pagination(
            callback: CallbackQuery, state: FSMContext
        ):
            parsed = parse_callback(callback.data)
            page_num = int(parsed.value)
            data = await state.get_data()
            pages = data.get("pages")

            if not pages or page_num >= len(pages):
                await callback.answer("❌ Страница не найдена")
                return

            await callback.message.edit_text(
                pages[page_num],
                parse_mode="HTML",
                reply_markup=self.get_pagination_keyboard(
                    page_num,
                    len(pages),
                ),
            )

            await state.update_data(current_page=page_num)
            await callback.answer()

    @abstractmethod
    def get_pagination_keyboard(
        self,
        current_page: int,
        total_pages: int,
    ):
        pass

    @property
    @abstractmethod
    def section_prefix(self) -> str:
        pass

    @property
    @abstractmethod
    def content_name(self) -> str:
        pass


class BaseYearSelectorHandler(BasePaginationHandler, ABC):
    """
    Базовый класс для выбора года и показа данных.
    """

    def __init__(self):
        super().__init__()
        self.callbacks = BaseCallbackFactory(self.section_prefix)
        self.calendar_year()
        self.value_type = None

    def calendar_year(self):
        @self.router.callback_query(
            lambda c: c.data.startswith(
                f"{self.callbacks.base_callback_year()}"
            )
            and "special" not in c.data
        )
        async def handle_year_selection(
            callback: CallbackQuery, state: FSMContext
        ):
            parsed = parse_callback(callback.data)
            value_type = parsed.value_type
            year = int(parsed.value)

            await callback.message.edit_text(
                f"⏳ Загрузка {self.content_name}..."
            )
            pages = await self.get_data_for_year(year, value_type)

            if not pages:
                await callback.message.edit_text(
                    NO_DATA_ERROR,
                    reply_markup=self.get_back_keyboard(),
                )
                await callback.answer()
                return

            await state.set_state(PaginationState.viewing)
            await state.update_data(pages=pages, current_page=0)

            await callback.message.edit_text(
                pages[0],
                parse_mode="HTML",
                reply_markup=self.get_pagination_keyboard(
                    0,
                    len(pages),
                ),
            )
            await callback.answer()

    @property
    @abstractmethod
    def section_prefix(self) -> str:
        pass

    @property
    @abstractmethod
    def content_name(self) -> str:
        pass

    @abstractmethod
    async def get_data_for_year(
        self, year: int, value_type: Optional[str] = None
    ) -> Optional[list[str]]:
        pass

    @abstractmethod
    def get_back_keyboard(self):
        pass
