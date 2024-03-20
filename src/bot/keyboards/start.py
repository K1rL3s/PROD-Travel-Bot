from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks import OpenMenu, ProfileData
from bot.utils.enums import Action, BotMenu, TextCommand

builder = InlineKeyboardBuilder()
for text, bot_menu in (
    (TextCommand.PROFILE, BotMenu.PROFILE),
    (TextCommand.TRAVELS, BotMenu.TRAVELS),
):
    builder.button(text=text, callback_data=OpenMenu(menu=bot_menu))
builder.adjust(1, repeat=True)

start_keyboard = builder.as_markup()

fill_profile_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="👋 Создать профиль",
                callback_data=ProfileData(action=Action.ADD).pack(),
            )
        ]
    ]
)
