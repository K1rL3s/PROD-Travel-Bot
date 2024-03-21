from aiogram import Bot, F, Router
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks import EditLocationData
from bot.filters import LocationCallbackOwner, LocationStateOwner
from bot.keyboards import (
    back_cancel_keyboard,
    cancel_keyboard,
    edit_location_keyboard,
    reply_keyboard_from_list,
)
from bot.utils.html import html_quote
from bot.utils.states import LocationState
from bot.utils.tg import delete_last_message
from core.models import LocationExtended, User
from core.services import GeoService, LocationService
from core.services.location import (
    get_location_field_validator,
    validate_city,
    validate_country,
)
from core.utils.enums import LocationField

from .funcs import format_location
from .phrases import CITY_ERROR, COUNTRY_ERROR, error_text_by_field

router = Router(name=__name__)


@router.callback_query(
    EditLocationData.filter(F.field.is_(None)),
    LocationCallbackOwner(),
)
async def edit_location(
    callback: CallbackQuery,
    callback_data: EditLocationData,
    location: LocationExtended,
) -> None:
    text = "Что вы хотите изменить?\n\n" + format_location(location)
    keyboard = edit_location_keyboard(callback_data.location_id, callback_data.page)
    await callback.message.edit_text(text=text, reply_markup=keyboard)


for field in (
    LocationField.TITLE,
    LocationField.ADDRESS,
    LocationField.START_AT,
    LocationField.END_AT,
):

    @router.callback_query(
        EditLocationData.filter(F.field == field),
        LocationCallbackOwner(),
    )
    async def edit_location_field(
        callback: CallbackQuery,
        callback_data: EditLocationData,
        state: FSMContext,
        location: LocationExtended,
    ) -> None:
        text = "Введите новое значение.\nТекущее: " + str(
            getattr(location, callback_data.field)
        )
        await callback.message.edit_text(text=text, reply_markup=back_cancel_keyboard)

        await state.set_state(LocationState.editing)
        await state.set_data(
            {
                "last_id": callback.message.message_id,
                "location_id": callback_data.location_id,
                "field": callback_data.field,
                "page": callback_data.page,
            },
        )


@router.message(F.text.as_("answer"), LocationState.editing, LocationStateOwner())
async def edit_field_entered(
    message: Message,
    bot: Bot,
    state: FSMContext,
    user: User,
    location: LocationExtended,
    location_service: LocationService,
    answer: str,
) -> None:
    data = await state.get_data()
    edit_field: str = data["field"]
    page: int = data["page"]

    validator = get_location_field_validator(edit_field)
    error_text = error_text_by_field[edit_field]
    if not validator(answer):
        await message.reply(text=error_text, reply_markup=back_cancel_keyboard)
        await delete_last_message(bot, state, message)
        return

    setattr(location, edit_field, html_quote(answer))
    await location_service.update_with_access_check(user.id, location.id, location)
    await message.answer(
        text=format_location(location),
        reply_markup=edit_location_keyboard(location.id, page),
    )
    await delete_last_message(bot, state, message)


@router.callback_query(
    or_f(
        EditLocationData.filter(F.field == LocationField.CITY),
        EditLocationData.filter(F.field == LocationField.COUNTRY),
    ),
    LocationCallbackOwner(),
)
async def edit_location_city_country(
    callback: CallbackQuery,
    callback_data: EditLocationData,
    state: FSMContext,
    location: LocationExtended,
) -> None:
    text = (
        "Так как не все города существуют во всех странах, "
        "то вам надо ввести и город, и страну. "
        "Начните с города, введите новое значение\n "
        f"Текущее: {getattr(location, 'city')}"
    )

    await callback.message.edit_text(text=text, reply_markup=cancel_keyboard)

    await state.set_state(LocationState.editing_city)
    await state.set_data(
        {
            "last_id": callback.message.message_id,
            "location_id": callback_data.location_id,
            "page": callback_data.page,
        },
    )


@router.message(
    F.text.as_("city"),
    LocationState.editing_city,
    LocationStateOwner(),
)
async def city_enter(
    message: Message,
    bot: Bot,
    state: FSMContext,
    location: LocationExtended,
    geo_service: GeoService,
    city: str,
) -> None:
    city = validate_city(city) and await geo_service.normalize_city(city)
    if city:
        text = f"Город есть, а из какой он страны?\nТекущая: {location.country}"
        countries = await geo_service.get_countries_by_city(city)
        keyboard = reply_keyboard_from_list(countries)
        await state.set_state(LocationState.editing_country)
        await state.update_data(city=city)
    else:
        text = CITY_ERROR
        keyboard = back_cancel_keyboard

    bot_msg = await message.answer(text=text, reply_markup=keyboard)
    await delete_last_message(bot, state, message)
    await state.update_data(last_id=bot_msg.message_id)


@router.message(
    F.text.as_("country"),
    LocationState.editing_country,
    LocationStateOwner(),
)
async def country_enter(
    message: Message,
    bot: Bot,
    state: FSMContext,
    location: LocationExtended,
    location_service: LocationService,
    geo_service: GeoService,
    country: str,
) -> None:
    text = COUNTRY_ERROR
    keyboard = cancel_keyboard
    if validate_country(country):
        data = await state.get_data()
        city_title: str = data["city"]
        page: int = data["page"]
        last_id: int = data["last_id"]

        country = await geo_service.normalize_country(country)
        countries = await geo_service.get_countries_by_city(city_title)
        if country and country.lower() in (c.lower() for c in countries):
            country = await geo_service.create_or_get_country(country)
            city = await geo_service.create_or_get_city(city_title, country.title)
            location.country_id = country.id
            location.city_id = city.id
            location = await location_service.update_with_access_check(
                message.from_user.id,
                location.id,
                location,
            )

            text = format_location(location)
            keyboard = edit_location_keyboard(location.id, page)
            await state.clear()
            await state.set_data({"last_id": last_id})

    bot_msg = await message.answer(text=text, reply_markup=keyboard)
    await delete_last_message(bot, state, message)
    await state.update_data(last_id=bot_msg.message_id)
