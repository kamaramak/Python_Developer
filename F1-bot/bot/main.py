import argparse
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeChat

from bot.config import (
    ADMIN_ID,
    BOT_TOKEN,
    DEBUG,
    LOCAL_TEST_BOT_TOKEN,
    TEST_BOT_TOKEN,
)
from bot.core.cache import init_cache
from bot.handlers import setup_handlers
from bot.middlewares import (
    KeyboardVersionMiddleware,
    TestModeMiddleware,
    UserTrackerMiddleware,
)
from bot.services.f1_data import F1DataService

bot_token = None
testing = False
local = False


def check_args():
    """Определяет токен в зависимости от флага --test"""
    global bot_token
    global testing
    global local

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="Запустить через тестового бота",
    )
    parser.add_argument(
        "-l",
        "--local",
        action="store_true",
        help="Запустить бота локально через тестового бота",
    )
    args = parser.parse_args()

    if args.test:
        bot_token = TEST_BOT_TOKEN
        testing = True
        print("🤖Запуск через ТЕСТОВОГО бота")
    elif args.local:
        bot_token = LOCAL_TEST_BOT_TOKEN
        testing = True
        local = True
        print("Запуск ЛОКАЛЬНО через ТЕСТОВОГО бота")
    else:
        bot_token = BOT_TOKEN
        print("🚀Запуск через ОСНОВОГО бота")


async def setup_bot_commands(bot: Bot):
    """Устанавливает команды для бота"""

    base_commands = [
        BotCommand(command="start", description="🚀Запуск(перезапуск) бота"),
        BotCommand(command="help", description="🆘Помощь"),
        BotCommand(
            command="privacy", description="🔐 Политика конфиденциальности"
        ),
        BotCommand(command="export_my_data", description="📦 Мои данные"),
        BotCommand(
            command="delete_my_data", description="🗑 Удалить мой аккаунт"
        ),
    ]

    admin_commands = base_commands + [
        BotCommand(command="userstats", description="📊 Статистика"),
        BotCommand(command="userlist", description="📋 Список пользователей"),
        BotCommand(command="userinfo", description="🔍 Информация"),
    ]

    # 1. Для всех остальных
    await bot.set_my_commands(
        commands=base_commands,
    )

    # 2. Для админа
    await bot.set_my_commands(
        commands=admin_commands,
        scope=BotCommandScopeChat(chat_id=ADMIN_ID),
    )


async def main():
    """Основная функция для запуска и работы бота."""
    # Проверка аргументов запуска
    check_args()

    await init_cache(testing=testing, local=local)

    # Настройка логирования
    logging.basicConfig(level=logging.INFO)

    # Инициализация сервисов
    f1_service = F1DataService()

    # Инициализация бота и диспетчера
    bot = Bot(token=bot_token)
    await setup_bot_commands(bot)
    dp = Dispatcher()
    if DEBUG:
        dp.message.middleware(TestModeMiddleware())
        dp.callback_query.middleware(TestModeMiddleware())

    dp.message.middleware(KeyboardVersionMiddleware())
    dp.callback_query.middleware(KeyboardVersionMiddleware())

    dp.message.middleware(UserTrackerMiddleware())
    dp.callback_query.middleware(UserTrackerMiddleware())

    # Подключение хендлеров с зависимостями
    setup_handlers(dp, f1_service)
    print(f"🚀 Бот запущен{' в локальном режиме!' if local else '!'}")
    polling_task = asyncio.create_task(dp.start_polling(bot))  # noqa
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
