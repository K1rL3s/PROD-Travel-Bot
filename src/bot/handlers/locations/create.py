from aiogram import F, Router, flags
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks import AddLocationData
from bot.filters import TravelCallbackOwner
from bot.keyboards import (
    cancel_keyboard,
    one_location_keyboard,
    reply_keyboard_from_list,
)
from bot.utils.datehelp import datetime_by_format
from bot.utils.format import format_location
from bot.utils.html import html_quote
from bot.utils.states import LocationCreating
from core.models import Location
from core.services import GeoService, LocationService
from core.services.location import (
    validate_address,
    validate_city,
    validate_country,
    validate_end_at,
    validate_start_at,
    validate_title,
)

from .phrases import (
    ADDRESS_ERROR,
    CITY_ERROR,
    COUNTRY_ERROR,
    DATETIME_ERROR,
    FILL_ADDRESS,
    FILL_CITY,
    FILL_COUNTRY,
    FILL_END_AT,
    FILL_START_AT,
    FILL_TITLE,
    LOCATION_ERROR,
    TITLE_ERROR,
)

router = Router(name=__name__)


@router.callback_query(AddLocationData.filter(), TravelCallbackOwner())
async def create_location(
    callback: CallbackQuery,
    callback_data: AddLocationData,
    state: FSMContext,
) -> None:
    text = FILL_TITLE
    await callback.message.answer(text=text, reply_markup=cancel_keyboard)

    await state.set_state(LocationCreating.title)
    await state.set_data(
        {
            "travel_id": callback_data.travel_id,
            "page": callback_data.page,
        }
    )


@router.message(F.text.as_("title"), LocationCreating.title)
async def title_entered(
    message: Message,
    state: FSMContext,
    title: str,
) -> None:
    if validate_title(title):
        text = FILL_CITY
        await state.update_data(title=title)
        await state.set_state(LocationCreating.city)
    else:
        text = TITLE_ERROR

    await message.answer(text=text, reply_markup=cancel_keyboard)


@router.message(F.text.as_("city"), LocationCreating.city)
@flags.processing
async def city_entered(
    message: Message,
    state: FSMContext,
    geo_service: GeoService,
    city: str,
) -> None:
    city = validate_city(city) and await geo_service.normalize_city(city)
    if city:
        text = FILL_COUNTRY
        countries = await geo_service.get_countries_by_city(city)
        keyboard = reply_keyboard_from_list(countries)
        await state.set_state(LocationCreating.country)
        await state.update_data(city=city)
    else:
        text = CITY_ERROR
        keyboard = cancel_keyboard

    await message.answer(text=text, reply_markup=keyboard)


@router.message(F.text.as_("country"), LocationCreating.country)
@flags.processing
async def country_entered(
    message: Message,
    state: FSMContext,
    geo_service: GeoService,
    country: str,
) -> None:
    if validate_country(country):
        country = await geo_service.normalize_country(country)
        data = await state.get_data()
        city: str = data["city"]
        countries = await geo_service.get_countries_by_city(city)
        if country and country.lower() in (c.lower() for c in countries):
            text = FILL_ADDRESS
            await state.set_state(LocationCreating.address)
            await state.update_data(country=country)
            address = await geo_service.get_location_address(
                data["title"],
                data["city"],
                country,
            )
            keyboard = (
                reply_keyboard_from_list([address.address])
                if address
                else cancel_keyboard
            )
        else:
            text = COUNTRY_ERROR
            keyboard = cancel_keyboard
    else:
        text = COUNTRY_ERROR
        keyboard = cancel_keyboard

    await message.answer(text=text, reply_markup=keyboard)


@router.message(F.text.as_("address"), LocationCreating.address)
async def address_entered(
    message: Message,
    state: FSMContext,
    address: str,
) -> None:
    if validate_address(address):
        text = FILL_START_AT
        await state.set_state(LocationCreating.start_at)
        await state.update_data(address=address)
    else:
        text = ADDRESS_ERROR

    await message.answer(text=text, reply_markup=cancel_keyboard)


@router.message(F.text.as_("start_at"), LocationCreating.start_at)
async def start_at_entered(
    message: Message,
    state: FSMContext,
    start_at: str,
) -> None:
    if validate_start_at(start_at):
        text = FILL_END_AT
        await state.set_state(LocationCreating.end_at)
        await state.update_data(start_at=start_at)
    else:
        text = DATETIME_ERROR

    await message.answer(text=text, reply_markup=cancel_keyboard)


@router.message(F.text.as_("end_at"), LocationCreating.end_at)
@flags.processing
async def end_at_entered(
    message: Message,
    state: FSMContext,
    location_service: LocationService,
    geo_service: GeoService,
    end_at: str,
) -> None:
    data = await state.get_data()
    start_at = datetime_by_format(data["start_at"])

    if not validate_end_at(end_at, start_at):
        text = DATETIME_ERROR
        await message.answer(text=text, reply_markup=cancel_keyboard)
        return

    country = await geo_service.create_or_get_country(data["country"])
    city = await geo_service.create_or_get_city(data["city"], country.title)
    address = await geo_service.get_location_address(
        data["title"], city.title, country.title
    )

    location = Location(
        travel_id=data["travel_id"],
        title=html_quote(data["title"]),
        city_id=city.id,
        country_id=country.id,
        address=html_quote(data["address"]),
        start_at=start_at,
        end_at=datetime_by_format(end_at),
        latitude=address.latitude if address else city.latitude,
        longitude=address.longitude if address else city.longitude,
    )
    location_ext = await location_service.create(location)

    text = format_location(location_ext)
    keyboard = one_location_keyboard(
        location_ext,
        message.from_user.id,
        page=data["page"],
    )
    await message.answer(text=text, reply_markup=keyboard)
    await state.clear()


@router.message(F.location, LocationCreating.city)
@flags.processing
async def location_entered(
    message: Message,
    state: FSMContext,
    geo_service: GeoService,
) -> None:
    reversed_geo = await geo_service.city_country_address_by_coords(
        message.location.latitude,
        message.location.longitude,
    )
    if reversed_geo:
        city, country, address = reversed_geo
        await state.update_data(
            city=city.title,
            country=country.title,
            address=address.address,
        )
        await state.set_state(LocationCreating.start_at)
        text = FILL_START_AT
    else:
        text = LOCATION_ERROR

    await message.answer(text=text, reply_markup=cancel_keyboard)
