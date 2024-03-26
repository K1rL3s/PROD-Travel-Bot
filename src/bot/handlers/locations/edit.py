from aiogram import Bot, F, Router, flags
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
from bot.utils.datehelp import datetime_by_format
from bot.utils.format import NO_DATA, format_datetime, format_location
from bot.utils.html import html_quote
from bot.utils.states import LocationState
from bot.utils.tg import delete_last_message
from core.models import LocationExtended, User
from core.services import GeoService, LocationService
from core.services.location import (
    get_location_field_validator,
    validate_city,
    validate_country,
    validate_start_at,
)
from core.utils.enums import LocationField

from .phrases import (
    CITY_ERROR,
    COUNTRY_ERROR,
    DATETIME_ERROR,
    EDIT_CITY_COUNTRY,
    EDIT_COUNTRY,
    LOCATION_ERROR,
    error_text_by_field,
)

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
    text = "❓ Что ты хочешь изменить?\n\n" + format_location(location)
    keyboard = edit_location_keyboard(callback_data.location_id, callback_data.page)
    await callback.message.edit_text(text=text, reply_markup=keyboard)


for field in (LocationField.TITLE, LocationField.ADDRESS):

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
        text = "Введи новое значение.\nТекущее: " + str(
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
    EditLocationData.filter(F.field == LocationField.START_AT),
    LocationCallbackOwner(),
)
async def edit_start_at(
    callback: CallbackQuery,
    callback_data: EditLocationData,
    state: FSMContext,
    location: LocationExtended,
) -> None:
    text = "Введи новое значение.\nТекущее: " + format_datetime(location.start_at)
    await callback.message.edit_text(text=text, reply_markup=back_cancel_keyboard)

    await state.set_state(LocationState.editing_start_at)
    await state.set_data(
        {
            "last_id": callback.message.message_id,
            "location_id": callback_data.location_id,
            "field": "start_at",
            "page": callback_data.page,
        },
    )


@router.message(
    F.text.as_("start_at"),
    LocationState.editing_start_at,
    LocationStateOwner(),
)
async def start_at_entered(
    message: Message,
    bot: Bot,
    state: FSMContext,
    location_service: LocationService,
    location: LocationExtended,
    start_at: str,
) -> None:
    if not validate_start_at(start_at):
        text = DATETIME_ERROR
        keyboard = back_cancel_keyboard
    else:
        location.start_at = datetime_by_format(start_at)
        await location_service.update_with_access_check(
            message.from_user.id, location.id, location
        )

        data = await state.get_data()
        page: int = data["page"]
        last_id: int = data["last_id"]

        text = format_location(location)
        keyboard = edit_location_keyboard(location.id, page)
        await state.clear()
        await state.set_data({"last_id": last_id})

    bot_msg = await message.answer(text=text, reply_markup=keyboard)
    await delete_last_message(bot, state, message)
    await state.update_data(last_id=bot_msg.message_id)


@router.callback_query(
    or_f(
        EditLocationData.filter(F.field == LocationField.CITY),
        EditLocationData.filter(F.field == LocationField.COUNTRY),
    ),
    LocationCallbackOwner(),
)
async def edit_city_or_country(
    callback: CallbackQuery,
    callback_data: EditLocationData,
    state: FSMContext,
    location: LocationExtended,
) -> None:
    text = EDIT_CITY_COUNTRY.format(value=location.city.title)
    await callback.message.edit_text(text=text, reply_markup=cancel_keyboard)

    await state.set_state(LocationState.editing_city)
    await state.set_data(
        {"location_id": callback_data.location_id, "page": callback_data.page},
    )


@router.message(
    F.text.as_("city"),
    LocationState.editing_city,
    LocationStateOwner(),
)
@flags.processing
async def city_enter(
    message: Message,
    state: FSMContext,
    location: LocationExtended,
    geo_service: GeoService,
    city: str,
) -> None:
    city = validate_city(city) and await geo_service.normalize_city(city)
    if city:
        text = EDIT_COUNTRY.format(country=location.country.title)
        countries = await geo_service.get_countries_by_city(city)
        keyboard = reply_keyboard_from_list(countries)
        await state.set_state(LocationState.editing_country)
        await state.update_data(city=city)
    else:
        text = CITY_ERROR
        keyboard = back_cancel_keyboard

    await message.answer(text=text, reply_markup=keyboard)


@router.message(
    F.text.as_("country"),
    LocationState.editing_country,
    LocationStateOwner(),
)
@flags.processing
async def country_enter(
    message: Message,
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

        country = await geo_service.normalize_country(country)
        countries = await geo_service.get_countries_by_city(city_title)
        if country and country.lower() in (c.lower() for c in countries):
            country = await geo_service.create_or_get_country(country)
            city = await geo_service.create_or_get_city(city_title, country.title)
            location.country_id = country.id
            location.city_id = city.id

            address = await geo_service.get_location_address(
                location.title, city.title, country.title
            )
            if address:
                location.latitude = address.latitude
                location.longitude = address.longitude
                location.address = address.address
            else:
                location.address = NO_DATA

            location = await location_service.update_with_access_check(
                message.from_user.id,
                location.id,
                location,
            )

            text = format_location(location)
            keyboard = edit_location_keyboard(location.id, page)
            await state.clear()

    await message.answer(text=text, reply_markup=keyboard)


@router.message(F.location, LocationState.editing_city, LocationStateOwner())
@flags.processing
async def location_entered(
    message: Message,
    state: FSMContext,
    geo_service: GeoService,
    location_service: LocationService,
    location: LocationExtended,
) -> None:
    reversed_geo = await geo_service.city_country_address_by_coords(
        message.location.latitude,
        message.location.longitude,
    )
    if reversed_geo:
        city, country, address = reversed_geo
        location.city_id = city.id
        location.country_id = country.id
        location.address = address.address
        location = await location_service.update_with_access_check(
            message.from_user.id, location.id, location
        )

        data = await state.get_data()
        page: int = data["page"]
        await state.clear()

        text = format_location(location)
        keyboard = edit_location_keyboard(location.id, page)
    else:
        text = LOCATION_ERROR
        keyboard = cancel_keyboard

    await message.answer(text=text, reply_markup=keyboard)
