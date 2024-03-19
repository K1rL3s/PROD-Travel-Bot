from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.callbacks.menu import OpenMenu
from bot.callbacks.state import InStateData
from bot.utils.enums import Action, BotMenu

YES = "✅"
NO = "❌"
BACK = "🔙"
ADD = "➕"
EDIT = "✏️"
GET = "🔍"
DELETE = "🗑️"
TRAVEL = "✈️"
LOCATION = "🗽"
NOTE = "📝"
START = "🏠"


back_button = InlineKeyboardButton(
    text=f"{BACK} Назад",
    callback_data=InStateData(action=Action.BACK).pack(),
)
cancel_button = InlineKeyboardButton(
    text=f"{NO} Отмена",
    callback_data=InStateData(action=Action.CANCEL).pack(),
)
start_button = InlineKeyboardButton(
    text=f"{START} Меню",
    callback_data=OpenMenu(menu=BotMenu.START).pack(),
)


cancel_keyboard = InlineKeyboardMarkup(inline_keyboard=[[cancel_button]])
back_cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[back_button, cancel_button]]
)
