from aiogram import F, Router, flags
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks import ProfileData
from bot.keyboards import (
    after_registration_keyboard,
    cancel_keyboard,
    reply_keyboard_from_list,
)
from bot.utils.enums import Action
from bot.utils.format import NO_DATA
from bot.utils.html import html_quote
from bot.utils.states import ProfileCreating
from core.models import User
from core.services import GeoService, UserService
from core.services.user import (
    validate_age,
    validate_city,
    validate_country,
    validate_name,
)

from .phrases import (
    AGE_ERROR,
    ALL_RIGHT_BRO,
    CITY_ERROR,
    COUNTRY_ERROR,
    FILL_AGE,
    FILL_CITY,
    FILL_COUNTRY,
    FILL_NAME,
    LOCATION_ERROR,
    NAME_ERROR,
)

router = Router(name=__name__)


@router.callback_query(ProfileData.filter(F.action == Action.ADD))
async def start_create_profile(callback: CallbackQuery, state: FSMContext) -> None:
    text = FILL_NAME
    await callback.message.answer(text=text, reply_markup=cancel_keyboard)
    await state.clear()
    await state.set_state(ProfileCreating.name)


@router.message(F.text.as_("name"), ProfileCreating.name)
async def name_entered(
    message: Message,
    state: FSMContext,
    name: str,
) -> None:
    if validate_name(name):
        text = FILL_AGE.format(name=html_quote(name))
        await state.set_state(ProfileCreating.age)
        await state.update_data(name=name)
    else:
        text = NAME_ERROR

    await message.answer(text=text, reply_markup=cancel_keyboard)


@router.message(F.text.as_("age"), ProfileCreating.age)
async def age_entered(
    message: Message,
    state: FSMContext,
    age: str,
) -> None:
    if validate_age(age):
        text = FILL_CITY.format(age=int(age))
        await state.set_state(ProfileCreating.city)
        await state.update_data(age=age)
    else:
        text = AGE_ERROR

    await message.answer(text=text, reply_markup=cancel_keyboard)


@router.message(F.text.as_("city"), ProfileCreating.city)
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
        await state.set_state(ProfileCreating.country)
        await state.update_data(city=city)
        countries = await geo_service.get_countries_by_city(city)
        keyboard = reply_keyboard_from_list(countries)
    else:
        text = CITY_ERROR
        keyboard = cancel_keyboard

    await message.answer(text=text, reply_markup=keyboard)


@router.message(F.text.as_("country_title"), ProfileCreating.country)
@flags.processing
async def country_entered(
    message: Message,
    state: FSMContext,
    geo_service: GeoService,
    user_service: UserService,
    country_title: str,
) -> None:
    text = COUNTRY_ERROR
    keyboard = cancel_keyboard
    if validate_country(country_title):
        country_title = await geo_service.normalize_country(country_title)
        data = await state.get_data()
        city_title: str = data["city"]
        countries = await geo_service.get_countries_by_city(city_title)
        if country_title and country_title.lower() in (c.lower() for c in countries):
            text = ALL_RIGHT_BRO
            keyboard = after_registration_keyboard

            country = await geo_service.create_or_get_country(country_title)
            city = await geo_service.create_or_get_city(data["city"], country.title)
            user = User(
                id=message.from_user.id,
                tg_username=message.from_user.username,
                name=html_quote(data["name"]),
                age=int(data["age"]),
                city_id=city.id,
                country_id=country.id,
                description=NO_DATA,
            )
            await user_service.create(user)
            await state.clear()

    await message.answer(text=text, reply_markup=keyboard)


@router.message(F.location, ProfileCreating.city)
@flags.processing
async def location_entered(
    message: Message,
    state: FSMContext,
    geo_service: GeoService,
    user_service: UserService,
) -> None:
    reversed_geo = await geo_service.city_country_address_by_coords(
        message.location.latitude,
        message.location.longitude,
    )
    if reversed_geo:
        text = ALL_RIGHT_BRO
        keyboard = after_registration_keyboard
        city, country, _ = reversed_geo

        data = await state.get_data()
        await state.clear()

        user = User(
            id=message.from_user.id,
            tg_username=message.from_user.username,
            name=html_quote(data["name"]),
            age=int(data["age"]),
            city_id=city.id,
            country_id=country.id,
            description=NO_DATA,
        )
        await user_service.create(user)
    else:
        text = LOCATION_ERROR
        keyboard = cancel_keyboard

    await message.answer(text=text, reply_markup=keyboard)
