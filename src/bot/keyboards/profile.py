from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.menu import OpenMenu
from bot.callbacks.profile import EditProfileData, ProfileData
from bot.utils.enums import Action, BotMenu
from core.utils.enums import ProfileField

edit_profile_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✏️Изменить профиль",
                callback_data=ProfileData(action=Action.EDIT).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Назад",
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
    text="🔙 Назад",
    callback_data=OpenMenu(menu=BotMenu.PROFILE),
)
edit_profile_fields_keyboard = builder.adjust(1, repeat=True).as_markup()
