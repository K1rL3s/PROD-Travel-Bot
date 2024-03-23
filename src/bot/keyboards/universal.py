from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from bot.callbacks import InStateData, OpenMenu
from bot.utils.enums import Action, BotMenu

YES = "✅"
NO = "❌"
BACK = "🔙"
ADD = "➕"
INVITE = "🕊️"
EDIT = "✏️"
GET = "🔍"
DELETE = "🗑️"
PROFILE = "📖"
TRAVEL = "✈️"
LOCATION = "🗽"
NOTE = "📝"
START = "🏠"
MEMBER = "👫"


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


def reply_keyboard_from_list(strings: list[str]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        one_time_keyboard=True,
        resize_keyboard=True,
        keyboard=[[KeyboardButton(text=string)] for string in strings],
    )
