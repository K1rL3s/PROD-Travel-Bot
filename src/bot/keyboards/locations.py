from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.location import (
    AddLocationData,
    DeleteLocationData,
    EditLocationData,
    GetLocationData,
    LocationsPaginator,
)
from bot.callbacks.travel import GetTravelData
from bot.keyboards.paginate import paginate_keyboard
from bot.utils.enums import BotMenu
from core.models import LocationExtended
from core.service.location import LocationService
from core.service.travel import TravelService
from core.utils.enums import LocationField


async def locations_keyboard(
    tg_id: int,
    page: int,
    travel_id: int,
    location_service: LocationService,
    travel_service: TravelService,
) -> InlineKeyboardMarkup:
    rows, width = 6, 1
    subjects = [
        InlineKeyboardButton(
            text=location.title,
            callback_data=GetLocationData(
                location_id=location.id,
                page=page,
            ).pack(),
        )
        for location in await location_service.list_by_travel_id_with_access_check(
            tg_id,
            travel_id,
        )
    ]

    additional_buttons = []
    if await travel_service.is_owner(tg_id, travel_id):
        additional_buttons.append(
            InlineKeyboardButton(
                text="Добавить",
                callback_data=AddLocationData(
                    travel_id=travel_id,
                    page=page,
                ).pack(),
            )
        )

    additional_buttons.append(
        InlineKeyboardButton(
            text="Путешествие",
            callback_data=GetTravelData(travel_id=travel_id, page=page).pack(),
        )
    )

    return paginate_keyboard(
        buttons=subjects,
        menu=BotMenu.LOCATIONS,
        page=page,
        rows=rows,
        width=width,
        additional_buttons=additional_buttons,
        fabric=LocationsPaginator,
        travel_id=travel_id,
    )


def one_location_keyboard(
    location: LocationExtended,
    tg_id: int,
    page: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if location.travel.owner_id == tg_id:
        builder.row(
            InlineKeyboardButton(
                text="Редактировать",
                callback_data=EditLocationData(
                    location_id=location.id,
                    page=page,
                ).pack(),
            ),
            InlineKeyboardButton(
                text="Удалить",
                callback_data=DeleteLocationData(
                    location_id=location.id,
                    page=page,
                    sure=False,
                ).pack(),
            ),
        )

    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=LocationsPaginator(
                menu=BotMenu.TRAVELS,
                page=page,
                travel_id=location.travel_id,
            ).pack(),
        )
    )

    return builder.adjust(1, repeat=True).as_markup()


def edit_location_keyboard(location_id: int, page: int):
    builder = InlineKeyboardBuilder()
    for field_name, field_data in (
        ("1️⃣ Название", LocationField.TITLE),
        ("2️⃣ Страна", LocationField.COUNTRY),
        ("3️⃣ Город", LocationField.CITY),
        ("4️⃣ Адрес", LocationField.ADDRESS),
        ("5️⃣ Время начала", LocationField.START_AT),
        ("6️⃣ Время конца", LocationField.END_AT),
    ):
        builder.button(
            text=field_name,
            callback_data=EditLocationData(
                location_id=location_id,
                field=field_data,
                page=page,
            ),
        )
    builder.button(
        text="🔙 Назад",
        callback_data=GetLocationData(location_id=location_id, page=page),
    )
    return builder.adjust(1, repeat=True).as_markup()


def delete_location_keyboard(location_id: int, page: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Удалить",
                    callback_data=DeleteLocationData(
                        location_id=location_id,
                        page=page,
                        sure=True,
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=GetLocationData(
                        location_id=location_id,
                        page=page,
                    ).pack(),
                )
            ],
        ]
    )
