from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks import (
    AddTravelData,
    DeleteTravelData,
    EditTravelData,
    GetRouteData,
    GetTravelData,
    LeaveTravelData,
    LocationsPaginator,
    MembersPaginator,
    NotesPaginator,
    OpenMenu,
    RecommendPaginator,
)
from bot.keyboards.emoji import (
    ADD,
    BACK,
    DELETE,
    EDIT,
    GET,
    GET_OUT,
    LOCATION,
    MEMBER,
    NOTE,
    ROUTE,
    TRAVEL,
)
from bot.keyboards.paginate import paginate_keyboard
from bot.utils.enums import BotMenu
from core.models import Travel
from core.services import TravelService
from core.utils.enums import TravelField

MY_TRAVEL = "🔵"
NOT_MY_TRAVEL = "🟣"


def check_joined_travel(travel_id: int, travel_title) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{TRAVEL} {travel_title}",
                    callback_data=GetTravelData(travel_id=travel_id).pack(),
                )
            ]
        ]
    )


def back_to_travel_keyboard(travel_id: int, page: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{TRAVEL} Путешествие",
                    callback_data=GetTravelData(travel_id=travel_id, page=page).pack(),
                )
            ]
        ]
    )


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
            text=(MY_TRAVEL if travel.owner_id == tg_id else NOT_MY_TRAVEL)
            + " "
            + travel.title,
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
    builder.button(
        text=f"{ROUTE} Маршрут",
        callback_data=GetRouteData(page=page, travel_id=travel.id),
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
                text=f"{GET} Найти путешественников",
                callback_data=RecommendPaginator(
                    travel_id=travel.id,
                    page=page,
                ).pack(),
            ),
        )
    else:
        builder.row(
            InlineKeyboardButton(
                text=f"{GET_OUT} Покинуть путешествие",
                callback_data=LeaveTravelData(
                    travel_id=travel.id,
                    page=page,
                    sure=False,
                ).pack(),
            ),
        )

    builder.row(
        InlineKeyboardButton(
            text=f"{BACK} Все путешествия",
            callback_data=OpenMenu(menu=BotMenu.TRAVELS, page=page).pack(),
        )
    )

    return builder.as_markup()


def delete_travel_keyboard(travel_id: int, page: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{BACK} Назад",
                    callback_data=GetTravelData(
                        travel_id=travel_id,
                        page=page,
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text=f"{DELETE} Удалить",
                    callback_data=DeleteTravelData(
                        travel_id=travel_id,
                        page=page,
                        sure=True,
                    ).pack(),
                ),
            ],
        ]
    )


def edit_travel_keyboard(travel_id: int, page: int) -> InlineKeyboardMarkup:
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


def leave_travel_keyboard(travel_id: int, page: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{BACK} Назад",
                    callback_data=GetTravelData(
                        travel_id=travel_id,
                        page=page,
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text=f"{GET_OUT} Покинуть",
                    callback_data=LeaveTravelData(
                        travel_id=travel_id,
                        page=page,
                        sure=True,
                    ).pack(),
                ),
            ],
        ]
    )
