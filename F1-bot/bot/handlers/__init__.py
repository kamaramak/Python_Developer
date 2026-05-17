from aiogram import Router

from .admin import router as admin_router
from .calendar import setup as calendar_setup
from .commands import router as commands_router
from .common import router as common_router
from .results import setup as results_setup
from .standings import setup as standings_setup


def setup_handlers(router: Router, f1_service):
    """Подключаем все хендлеры"""

    # Простые роутеры без зависимостей
    router.include_router(commands_router)
    router.include_router(common_router)
    router.include_router(admin_router)

    # Роутеры с зависимостями
    calendar_setup(router, f1_service)
    standings_setup(router, f1_service)
    results_setup(router, f1_service)

    return router
