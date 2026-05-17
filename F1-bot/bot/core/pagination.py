from aiogram.fsm.state import State, StatesGroup


class PaginationState(StatesGroup):
    """Базовое состояние для пагинации"""

    viewing = State()
    pages = State()
    current_page = State()
    message_id = State()
