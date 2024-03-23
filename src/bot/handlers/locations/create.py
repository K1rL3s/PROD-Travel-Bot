from datetime import datetime

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks import AddLocationData
from bot.filters import TravelCallbackOwner
from bot.keyboards import (
    cancel_keyboard,
    one_location_keyboard,
    reply_keyboard_from_list,
)
from bot.utils.format import format_location
from bot.utils.html import html_quote
from bot.utils.states import LocationCreating
from bot.utils.tg import delete_last_message
from core.models import Location
from core.services import GeoService, LocationService
from core.services.location import (
    validate_address,
    validate_city,
    validate_country,
    validate_start_at,
)

from .phrases import (
    ADDRESS_ERROR,
    CITY_ERROR,
    COUNTRY_ERROR,
    FILL_ADDRESS,
    FILL_CITY,
    FILL_COUNTRY,
    FILL_START_AT,
    FILL_TITLE,
    START_AT_ERROR,
)

router = Router(name=__name__)


@router.callback_query(AddLocationData.filter(), TravelCallbackOwner())
async def create_location(
    callback: CallbackQuery,
    callback_data: AddLocationData,
    state: FSMContext,
) -> None:
    text = FILL_TITLE
    await callback.message.edit_text(text=text, reply_markup=cancel_keyboard)

    await state.set_state(LocationCreating.title)
    await state.set_data(
        {
            "last_id": callback.message.message_id,
            "travel_id": callback_data.travel_id,
            "page": callback_data.page,
        }
    )


@router.message(F.text.as_("title"), LocationCreating.title)
async def title_entered(
    message: Message,
    state: FSMContext,
    bot: Bot,
    title: str,
) -> None:
    text = FILL_CITY
    bot_msg = await message.answer(text=text, reply_markup=cancel_keyboard)

    await delete_last_message(bot, state, message)

    await state.set_state(LocationCreating.city)
    await state.update_data(title=title, last_id=bot_msg.message_id)


@router.message(F.text.as_("city"), LocationCreating.city)
async def city_entered(
    message: Message,
    state: FSMContext,
    bot: Bot,
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

    bot_msg = await message.answer(text=text, reply_markup=keyboard)

    await delete_last_message(bot, state, message)
    await state.update_data(last_id=bot_msg.message_id)


@router.message(F.text.as_("country"), LocationCreating.country)
async def country_entered(
    message: Message,
    state: FSMContext,
    bot: Bot,
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
            address = await geo_service.get_address(
                data["title"],
                data["city"],
                country,
            )
            keyboard = (
                reply_keyboard_from_list([address]) if address else cancel_keyboard
            )
        else:
            text = COUNTRY_ERROR
            keyboard = cancel_keyboard
    else:
        text = COUNTRY_ERROR
        keyboard = cancel_keyboard

    bot_msg = await message.answer(text=text, reply_markup=keyboard)

    await delete_last_message(bot, state, message)
    await state.update_data(last_id=bot_msg.message_id)


@router.message(F.text.as_("address"), LocationCreating.address)
async def address_entered(
    message: Message,
    state: FSMContext,
    bot: Bot,
    address: str,
) -> None:
    if validate_address(address):
        text = FILL_START_AT
        await state.set_state(LocationCreating.start_at)
        await state.update_data(address=address)
    else:
        text = ADDRESS_ERROR

    bot_msg = await message.answer(text=text, reply_markup=cancel_keyboard)

    await delete_last_message(bot, state, message)
    await state.update_data(last_id=bot_msg.message_id)


@router.message(F.text.as_("start_at"), LocationCreating.start_at)
async def start_at_entered(
    message: Message,
    state: FSMContext,
    bot: Bot,
    location_service: LocationService,
    geo_service: GeoService,
    start_at: str,
) -> None:
    if not validate_start_at(start_at):
        text = START_AT_ERROR
        bot_msg = await message.answer(text=text, reply_markup=cancel_keyboard)
        await delete_last_message(bot, state, message)
        await state.update_data(last_id=bot_msg.message_id)
        return

    data = await state.get_data()
    country = await geo_service.create_or_get_country(data["country"])
    city = await geo_service.create_or_get_city(data["city"], country.title)

    location = Location(
        travel_id=data["travel_id"],
        title=html_quote(data["title"]),
        city_id=city.id,
        country_id=country.id,
        address=html_quote(data["address"]),
        start_at=datetime.utcnow(),  # !!
    )
    location_ext = await location_service.create(location)

    text = format_location(location_ext)
    keyboard = one_location_keyboard(
        location_ext,
        message.from_user.id,
        page=data["page"],
    )
    await message.answer(text=text, reply_markup=keyboard)

    await delete_last_message(bot, state, message)
    await state.clear()
