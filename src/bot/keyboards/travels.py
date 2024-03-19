from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.locations import LocationsPaginator
from bot.callbacks.members import MembersPaginator
from bot.callbacks.menu import OpenMenu
from bot.callbacks.notes import NotesPaginator
from bot.callbacks.travels import (
    AddTravelData,
    DeleteTravelData,
    EditTravelData,
    GetTravelData,
)
from bot.keyboards.paginate import paginate_keyboard
from bot.keyboards.universal import ADD, BACK, DELETE, EDIT, LOCATION, MEMBER, NOTE
from bot.utils.enums import BotMenu
from core.models import Travel
from core.service.travel import TravelService
from core.utils.enums import TravelField


def back_to_travels_keyboard(page: int | None = 0) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{BACK} Назад",
                    callback_data=OpenMenu(menu=BotMenu.TRAVELS, page=page or 0).pack(),
                )
            ]
        ]
    )


async def travels_keyboard(
    tg_id: int,
    page: int,
    travel_service: TravelService,
) -> InlineKeyboardMarkup:
    rows, width = 6, 1
    subjects = [
        InlineKeyboardButton(
            text=travel.title,
            callback_data=GetTravelData(travel_id=travel.id, page=page).pack(),
        )
        for travel in await travel_service.list_by_tg_id(tg_id)
    ]

    create_travel_button = InlineKeyboardButton(
        text=f"{ADD} Создать путешествие",
        callback_data=AddTravelData(page=page).pack(),
    )

    return paginate_keyboard(
        buttons=subjects,
        menu=BotMenu.TRAVELS,
        page=page,
        rows=rows,
        width=width,
        additional_buttons=[create_travel_button],
    )


def one_travel_keyboard(
    travel: Travel,
    tg_id: int,
    page: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"{LOCATION} Локации",
        callback_data=LocationsPaginator(page=0, travel_id=travel.id),
    )
    builder.button(
        text=f"{NOTE} Заметки",
        callback_data=NotesPaginator(page=0, travel_id=travel.id),
    )
    builder.button(
        text=f"{MEMBER} Друзья",
        callback_data=MembersPaginator(page=0, travel_id=travel.id),
    )
    builder.adjust(1, repeat=True)

    if travel.owner_id == tg_id:
        builder.row(
            InlineKeyboardButton(
                text=f"{EDIT} Редактировать",
                callback_data=EditTravelData(
                    travel_id=travel.id,
                    page=page,
                ).pack(),
            ),
            InlineKeyboardButton(
                text=f"{DELETE} Удалить",
                callback_data=DeleteTravelData(
                    travel_id=travel.id,
                    page=page,
                    sure=False,
                ).pack(),
            ),
        )

    builder.row(
        InlineKeyboardButton(
            text=f"{BACK} Назад",
            callback_data=OpenMenu(menu=BotMenu.TRAVELS, page=page).pack(),
        )
    )

    return builder.as_markup()


def delete_travel_keyboard(travel_id: int, page: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{DELETE} Удалить",
                    callback_data=DeleteTravelData(
                        travel_id=travel_id,
                        page=page,
                        sure=True,
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{BACK} Назад",
                    callback_data=GetTravelData(
                        travel_id=travel_id,
                        page=page,
                    ).pack(),
                )
            ],
        ]
    )


def edit_travel_keyboard(travel_id: int, page: int):
    builder = InlineKeyboardBuilder()
    for field_name, field_data in (
        ("1️⃣ Название", TravelField.TITLE),
        ("2️⃣ Описание", TravelField.DESCRIPTION),
    ):
        builder.button(
            text=field_name,
            callback_data=EditTravelData(
                travel_id=travel_id,
                field=field_data,
                page=page,
            ),
        )
    builder.button(
        text=f"{BACK} Назад",
        callback_data=GetTravelData(travel_id=travel_id, page=page),
    )
    return builder.adjust(1, repeat=True).as_markup()
