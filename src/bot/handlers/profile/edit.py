from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks import EditProfileData, InStateData, ProfileData
from bot.keyboards import (
    back_cancel_keyboard,
    cancel_keyboard,
    edit_profile_fields_keyboard,
    reply_keyboard_from_list,
)
from bot.utils.enums import Action
from bot.utils.format import format_user_profile
from bot.utils.html import html_quote
from bot.utils.states import ProfileState
from bot.utils.tg import delete_last_message
from core.models import User, UserExtended
from core.services import GeoService, UserService
from core.services.user import get_user_field_validator, validate_city, validate_country
from core.utils.enums import ProfileField

from .phrases import CITY_ERROR, COUNTRY_ERROR, error_text_by_field

router = Router(name=__name__)


@router.callback_query(ProfileData.filter(F.action == Action.EDIT))
@router.callback_query(
    InStateData.filter(F.action == Action.BACK),
    ProfileState.editing,
)
async def edit_profile(callback: CallbackQuery, user: UserExtended) -> None:
    text = "Что вы хотите изменить?\n\n" + format_user_profile(user)
    keyboard = edit_profile_fields_keyboard
    await callback.message.edit_text(text=text, reply_markup=keyboard)


for field in (ProfileField.NAME, ProfileField.AGE, ProfileField.DESCRIPTION):

    @router.callback_query(EditProfileData.filter(F.field == field))
    async def edit_profile_field(
        callback: CallbackQuery,
        callback_data: EditProfileData,
        state: FSMContext,
        user: User,
    ) -> None:
        text = "Введите новое значение.\nТекущее: " + str(
            getattr(user, callback_data.field)
        )
        await callback.message.edit_text(text=text, reply_markup=back_cancel_keyboard)
        await state.set_data(
            {
                "last_id": callback.message.message_id,
                "field": callback_data.field,
            },
        )
        await state.set_state(ProfileState.editing)


@router.message(F.text.as_("answer"), ProfileState.editing)
async def field_entered(
    message: Message,
    bot: Bot,
    state: FSMContext,
    user: UserExtended,
    user_service: UserService,
    answer: str,
) -> None:
    data = await state.get_data()
    edit_field: str = data["field"]
    validator = get_user_field_validator(edit_field)
    error_text = error_text_by_field[edit_field]

    if not validator(answer):
        await message.reply(text=error_text, reply_markup=back_cancel_keyboard)
        await delete_last_message(bot, state, message)
        return

    setattr(user, edit_field, html_quote(answer))
    await user_service.update(user.id, user)
    await message.answer(
        text=format_user_profile(user),
        reply_markup=edit_profile_fields_keyboard,
    )
    await delete_last_message(bot, state, message)
    await state.clear()


@router.callback_query(EditProfileData.filter(F.field == ProfileField.CITY))
@router.callback_query(EditProfileData.filter(F.field == ProfileField.COUNTRY))
async def edit_profile_city_country(
    callback: CallbackQuery,
    state: FSMContext,
    user: User,
) -> None:
    text = (
        "Так как не все города существуют во всех странах, "
        "то вам надо ввести и город, и страну. "
        "Начните с города, введите новое значение\n "
        f"Текущее: {getattr(user, 'city')}"
    )

    await callback.message.edit_text(text=text, reply_markup=cancel_keyboard)
    await state.set_data({"last_id": callback.message.message_id})
    await state.set_state(ProfileState.editing_city)


@router.message(
    F.text.as_("city"),
    ProfileState.editing_city,
)
async def city_enter(
    message: Message,
    bot: Bot,
    state: FSMContext,
    user: UserExtended,
    geo_service: GeoService,
    city: str,
) -> None:
    city = validate_city(city) and await geo_service.normalize_city(city)
    if city:
        text = f"Город есть, а из какой он страны?\nТекущая: {user.country}"
        countries = await geo_service.get_countries_by_city(city)
        keyboard = reply_keyboard_from_list(countries)
        await state.set_state(ProfileState.editing_country)
        await state.update_data(city=city)
    else:
        text = CITY_ERROR
        keyboard = back_cancel_keyboard

    bot_msg = await message.answer(text=text, reply_markup=keyboard)
    await delete_last_message(bot, state, message)
    await state.update_data(last_id=bot_msg.message_id)


@router.message(
    F.text.as_("country"),
    ProfileState.editing_country,
)
async def country_enter(
    message: Message,
    bot: Bot,
    state: FSMContext,
    user: UserExtended,
    user_service: UserService,
    geo_service: GeoService,
    country: str,
) -> None:
    text = COUNTRY_ERROR
    keyboard = cancel_keyboard
    if validate_country(country):
        data = await state.get_data()
        city_title: str = data["city"]
        last_id: int = data["last_id"]

        country = await geo_service.normalize_country(country)
        countries = await geo_service.get_countries_by_city(city_title)
        if country and country.lower() in (c.lower() for c in countries):
            country = await geo_service.create_or_get_country(country)
            city = await geo_service.create_or_get_city(city_title, country.title)
            user.country_id = country.id
            user.city_id = city.id
            user = await user_service.update(user.id, user)

            text = format_user_profile(user)
            keyboard = edit_profile_fields_keyboard
            await state.clear()
            await state.set_data({"last_id": last_id})

    bot_msg = await message.answer(text=text, reply_markup=keyboard)
    await delete_last_message(bot, state, message)
    await state.update_data(last_id=bot_msg.message_id)
