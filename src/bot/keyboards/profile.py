from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks import EditProfileData, OpenMenu, Paginator, ProfileData
from bot.keyboards.emoji import BACK, EDIT, PROFILE, TRAVEL
from bot.utils.enums import Action, BotMenu
from core.utils.enums import ProfileField

after_registration_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data=data)]
        for (text, data) in (
            (
                f"{EDIT} Добавить описание",
                EditProfileData(field=ProfileField.DESCRIPTION).pack(),
            ),
            (f"{PROFILE} Профиль", ProfileData(action=Action.GET).pack()),
            (f"{TRAVEL} Путешествия", Paginator(menu=BotMenu.TRAVELS, page=0).pack()),
        )
    ]
)


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
                text=f"{BACK} Меню",
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
    ("4️⃣ Страна", ProfileField.COUNTRY),
    ("5️⃣ Описание", ProfileField.DESCRIPTION),
):
    builder.button(text=field_name, callback_data=EditProfileData(field=field_data))
builder.button(
    text=f"{BACK} Профиль",
    callback_data=OpenMenu(menu=BotMenu.PROFILE),
)
edit_profile_fields_keyboard = builder.adjust(1, repeat=True).as_markup()
