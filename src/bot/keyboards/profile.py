from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.menu import OpenMenu
from bot.callbacks.profile import EditProfileData, ProfileData
from bot.keyboards.universal import BACK, EDIT
from bot.utils.enums import Action, BotMenu
from core.utils.enums import ProfileField

edit_profile_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"{EDIT} Изменить профиль",
                callback_data=ProfileData(action=Action.EDIT).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=f"{BACK} Назад",
                callback_data=OpenMenu(menu=BotMenu.START).pack(),
            )
        ],
    ]
)

builder = InlineKeyboardBuilder()
for field_name, field_data in (
    ("1️⃣ Имя", ProfileField.NAME),
    ("2️⃣ Возраст", ProfileField.AGE),
    ("3️⃣ Город", ProfileField.CITY),
    ("4️⃣ Описание", ProfileField.DESCRIPTION),
):
    builder.button(text=field_name, callback_data=EditProfileData(field=field_data))
builder.button(
    text=f"{BACK} Назад",
    callback_data=OpenMenu(menu=BotMenu.PROFILE),
)
edit_profile_fields_keyboard = builder.adjust(1, repeat=True).as_markup()


def choose_country(countries: list[str]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        one_time_keyboard=True,
        resize_keyboard=True,
        keyboard=[[KeyboardButton(text=country)] for country in countries],
    )
