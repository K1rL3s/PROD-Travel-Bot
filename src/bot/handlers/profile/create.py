from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks import ProfileData
from bot.keyboards import (
    after_registration_keyboard,
    cancel_keyboard,
    reply_keyboard_from_list,
)
from bot.utils.enums import Action
from bot.utils.html import html_quote
from bot.utils.states import ProfileCreating
from bot.utils.tg import delete_last_message
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
    NAME_ERROR,
)

router = Router(name=__name__)


@router.callback_query(ProfileData.filter(F.action == Action.ADD))
async def start_create_profile(callback: CallbackQuery, state: FSMContext) -> None:
    text = FILL_NAME
    await callback.message.answer(text=text, reply_markup=cancel_keyboard)
    await state.clear()
    await state.set_state(ProfileCreating.name)
    await state.set_data({"last_id": callback.message.message_id})


@router.message(F.text.as_("name"), ProfileCreating.name)
async def name_entered(
    message: Message,
    bot: Bot,
    state: FSMContext,
    name: str,
) -> None:
    if validate_name(name):
        text = FILL_AGE.format(name=html_quote(name))
        await state.set_state(ProfileCreating.age)
        await state.update_data(name=name)
    else:
        text = NAME_ERROR

    bot_msg = await message.answer(text=text, reply_markup=cancel_keyboard)
    await delete_last_message(bot, state, message)
    await state.update_data(last_id=bot_msg.message_id)


@router.message(F.text.as_("age"), ProfileCreating.age)
async def age_entered(
    message: Message,
    bot: Bot,
    state: FSMContext,
    age: str,
) -> None:
    if validate_age(age):
        text = FILL_CITY.format(age=int(age))
        await state.set_state(ProfileCreating.city)
        await state.update_data(age=age)
    else:
        text = AGE_ERROR

    bot_msg = await message.answer(text=text, reply_markup=cancel_keyboard)
    await delete_last_message(bot, state, message)
    await state.update_data(last_id=bot_msg.message_id)


@router.message(F.text.as_("city"), ProfileCreating.city)
async def city_entered(
    message: Message,
    bot: Bot,
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

    bot_msg = await message.answer(text=text, reply_markup=keyboard)
    await delete_last_message(bot, state, message)
    await state.update_data(last_id=bot_msg.message_id)


@router.message(F.text.as_("country_title"), ProfileCreating.country)
async def country_entered(
    message: Message,
    bot: Bot,
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
                description=None,
            )
            await user_service.create(user)
            await state.clear()
            await state.update_data(last_id=data["last_id"])

    bot_msg = await message.answer(text=text, reply_markup=keyboard)
    await delete_last_message(bot, state, message)
    await state.update_data(last_id=bot_msg.message_id)
