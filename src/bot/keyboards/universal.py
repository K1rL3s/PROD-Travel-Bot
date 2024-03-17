from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.callbacks.menu import OpenMenu
from bot.callbacks.state import InStateData
from bot.utils.enums import Action, BotMenu

back_button = InlineKeyboardButton(
    text="🔙 Назад",
    callback_data=InStateData(action=Action.BACK).pack(),
)
cancel_button = InlineKeyboardButton(
    text="🚫 Отмена",
    callback_data=InStateData(action=Action.CANCEL).pack(),
)
start_button = InlineKeyboardButton(
    text="Меню",
    callback_data=OpenMenu(menu=BotMenu.START).pack(),
)


back_cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[back_button, cancel_button]]
)
