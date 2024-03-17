from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.callbacks.state import InStateData
from bot.utils.enums import Action

back_button = InlineKeyboardButton(
    text="🔙 Назад",
    callback_data=InStateData(action=Action.BACK).pack(),
)
cancel_button = InlineKeyboardButton(
    text="🚫 Отмена",
    callback_data=InStateData(action=Action.CANCEL).pack(),
)


back_cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[back_button, cancel_button]]
)
