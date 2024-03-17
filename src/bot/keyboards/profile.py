from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.menu import OpenMenu
from bot.callbacks.profile import EditProfileData, ProfileData
from bot.utils.enums import Action, BotMenu, ProfileFields

check_profile_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📖Мой профиль",
                callback_data=ProfileData(action=Action.GET).pack(),
            )
        ]
    ]
)
fill_profile_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="👋Зарегистрироваться",
                callback_data=ProfileData(action=Action.ADD).pack(),
            )
        ]
    ]
)
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
    ("1️⃣ Имя", ProfileFields.NAME),
    ("2️⃣ Возраст", ProfileFields.AGE),
    ("3️⃣ Город", ProfileFields.CITY),
    ("4️⃣ Описание", ProfileFields.DESCRIPTION),
):
    builder.button(text=field_name, callback_data=EditProfileData(field=field_data))
builder.button(
    text="🔙 Назад",
    callback_data=OpenMenu(menu=BotMenu.PROFILE),
)
edit_profile_fields_keyboard = builder.adjust(1, repeat=True).as_markup()
