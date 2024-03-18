from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.location import LocationPaginator
from bot.callbacks.menu import OpenMenu
from bot.callbacks.travel import (
    AddTravelData,
    DeleteTravelData,
    EditTravelData,
    GetTravelData,
)
from bot.keyboards.paginate import paginate_keyboard
from bot.utils.enums import Action, BotMenu
from core.models import Travel
from core.service.travel import TravelService
from core.utils.enums import TravelField


def back_to_travels_keyboard(page: int | None = 0) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Назад",
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
        text="Создать путешествие",
        callback_data=AddTravelData(action=Action.ADD, page=page).pack(),
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
        text="Локации",
        callback_data=LocationPaginator(
            menu=BotMenu.LOCATIONS,
            page=0,
            travel_id=travel.id,
            travels_page=page,
        ),
    )
    builder.adjust(1, repeat=True)

    if travel.owner_id == tg_id:
        builder.row(
            InlineKeyboardButton(
                text="Редактировать",
                callback_data=EditTravelData(
                    travel_id=travel.id,
                    page=page,
                ).pack(),
            ),
            InlineKeyboardButton(
                text="Удалить",
                callback_data=DeleteTravelData(
                    travel_id=travel.id,
                    page=page,
                    sure=False,
                ).pack(),
            ),
        )

    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=OpenMenu(menu=BotMenu.TRAVELS, page=page).pack(),
        )
    )

    return builder.as_markup()


def delete_travel_keyboard(travel_id: int, page: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Удалить",
                    callback_data=DeleteTravelData(
                        travel_id=travel_id,
                        page=page,
                        sure=True,
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
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
        text="🔙 Назад",
        callback_data=GetTravelData(travel_id=travel_id, page=page),
    )
    return builder.adjust(1, repeat=True).as_markup()
