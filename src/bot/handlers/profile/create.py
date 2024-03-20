from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.profile import ProfileData
from bot.handlers.profile.phrases import (
    AGE_ERROR,
    CITY_ERROR,
    COUNTRY_ERROR,
    DESCRIPTION_ERROR,
    NAME_ERROR,
)
from bot.keyboards.start import start_keyboard
from bot.keyboards.universal import cancel_keyboard, reply_keyboard_from_list
from bot.utils.enums import Action
from bot.utils.html import html_quote
from bot.utils.states import ProfileCreating
from bot.utils.tg import delete_last_message
from core.models import User
from core.service.geo import GeoService
from core.service.user import (
    UserService,
    validate_age,
    validate_city,
    validate_country,
    validate_description,
    validate_name,
)

router = Router(name=__name__)


@router.callback_query(ProfileData.filter(F.action == Action.ADD))
async def start_create_profile(callback: CallbackQuery, state: FSMContext) -> None:
    text = "Как вас зовут?"
    await callback.message.edit_text(text=text, reply_markup=cancel_keyboard)
    await state.set_state(ProfileCreating.name)
    await state.set_data({"last_id": callback.message.message_id})


@router.message(F.text.as_("name"), ProfileCreating.name)
async def profile_name_entered(
    message: Message,
    bot: Bot,
    state: FSMContext,
    name: str,
) -> None:
    if validate_name(name):
        text = "Сколько вам лет?"
        await state.set_state(ProfileCreating.age)
        await state.update_data(name=name)
    else:
        text = NAME_ERROR

    bot_msg = await message.answer(text=text, reply_markup=cancel_keyboard)
    await delete_last_message(bot, state, message)
    await state.update_data(last_id=bot_msg.message_id)


@router.message(F.text.as_("age"), ProfileCreating.age)
async def profile_age_entered(
    message: Message,
    bot: Bot,
    state: FSMContext,
    age: str,
) -> None:
    if validate_age(age):
        text = "В каком городе вы живёте?"
        await state.set_state(ProfileCreating.city)
        await state.update_data(age=age)
    else:
        text = AGE_ERROR

    bot_msg = await message.answer(text=text, reply_markup=cancel_keyboard)
    await delete_last_message(bot, state, message)
    await state.update_data(last_id=bot_msg.message_id)


@router.message(F.text.as_("city"), ProfileCreating.city)
async def profile_city_entered(
    message: Message,
    bot: Bot,
    state: FSMContext,
    geo_service: GeoService,
    city: str,
) -> None:
    city = validate_city(city) and await geo_service.normalize_city(city)
    if city:
        text = "Из какой вы страны?"
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


@router.message(F.text.as_("country"), ProfileCreating.country)
async def profile_country_entered(
    message: Message,
    bot: Bot,
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
            text = "Расскажите о себе. Это будет описанием вашего профиля."
            await state.set_state(ProfileCreating.descirption)
            await state.update_data(country=country)
        else:
            text = COUNTRY_ERROR
    else:
        text = COUNTRY_ERROR

    bot_msg = await message.answer(text=text, reply_markup=cancel_keyboard)
    await delete_last_message(bot, state, message)
    await state.update_data(last_id=bot_msg.message_id)


@router.message(F.text.as_("description"), ProfileCreating.descirption)
async def profile_description_entered(
    message: Message,
    bot: Bot,
    state: FSMContext,
    user_service: UserService,
    description: str,
) -> None:
    if not validate_description(description):
        text = DESCRIPTION_ERROR
        await message.answer(text=text, reply_markup=cancel_keyboard)
        await delete_last_message(bot, state, message)
        return

    await message.answer(
        text="Профиль успешно создан!",
        reply_markup=start_keyboard,
    )

    data = await state.get_data()
    user = User(
        id=message.from_user.id,
        name=html_quote(data["name"]),
        age=int(data["age"]),
        city=html_quote(data["city"]),
        country=html_quote(data["country"]),
        description=html_quote(description),
    )
    await user_service.create(user)

    await delete_last_message(bot, state, message)
    await state.set_data({})
