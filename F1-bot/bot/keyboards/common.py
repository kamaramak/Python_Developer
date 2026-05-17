"""Общие инлайн-клавиатуры: назад, закрыть, подтверждение"""

from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.core.callbacks import BaseCallbackFactory


def get_back_keyboard(section_prefix: str):
    """
    Кнопка "Назад" - универсальная
    Можно использовать для возврата в меню, к выбору года и т.д.
    """
    callbacks = BaseCallbackFactory(section_prefix)
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔙 В меню", callback_data=callbacks.callback_back_to_menu()
    )
    return builder.as_markup()


__all__ = ["get_back_keyboard"]
