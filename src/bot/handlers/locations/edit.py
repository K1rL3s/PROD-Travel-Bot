from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.locations import EditLocationData
from bot.filters.locations import LocationCallbackOwner, LocationStateOwner
from bot.filters.universal import FieldInState
from bot.keyboards.locations import edit_location_keyboard
from bot.keyboards.universal import back_cancel_keyboard
from bot.utils.html import html_quote
from bot.utils.states import LocationState
from bot.utils.tg import delete_last_message
from core.models import LocationExtended, User
from core.service.geo import GeoService
from core.service.location import (
    LocationService,
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


for field in LocationField.values():

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

        await state.set_data(
            {
                "last_id": callback.message.message_id,
                "location_id": callback_data.location_id,
                "field": callback_data.field,
                "page": callback_data.page,
            },
        )
        await state.set_state(LocationState.editing)


@router.message(
    F.text.as_("city"),
    LocationState.editing,
    LocationStateOwner(),
    FieldInState("city"),
)
async def edit_city_entered(
    message: Message,
    bot: Bot,
    state: FSMContext,
    user: User,
    location: LocationExtended,
    location_service: LocationService,
    geo_service: GeoService,
    city: str,
) -> None:
    data = await state.get_data()
    edit_field = "city"
    page: int = data["page"]

    city = validate_city(city) and await geo_service.normalize_city(city)
    if not city:
        await message.reply(text=CITY_ERROR, reply_markup=back_cancel_keyboard)
        await delete_last_message(bot, state, message)
        return

    setattr(location, edit_field, html_quote(city))
    await location_service.update_with_access_check(user.id, location.id, location)
    await message.answer(
        text=format_location(location),
        reply_markup=edit_location_keyboard(location.id, page),
    )
    await delete_last_message(bot, state, message)


@router.message(
    F.text.as_("country"),
    LocationState.editing,
    LocationStateOwner(),
    FieldInState("country"),
)
async def edit_country_entered(
    message: Message,
    bot: Bot,
    state: FSMContext,
    user: User,
    location: LocationExtended,
    location_service: LocationService,
    geo_service: GeoService,
    country: str,
) -> None:
    data = await state.get_data()
    edit_field = "country"
    page: int = data["page"]

    country = validate_country(country) and await geo_service.normalize_country(country)
    if not country:
        await message.reply(text=COUNTRY_ERROR, reply_markup=back_cancel_keyboard)
        await delete_last_message(bot, state, message)
        return

    setattr(location, edit_field, html_quote(country))
    await location_service.update_with_access_check(user.id, location.id, location)
    await message.answer(
        text=format_location(location),
        reply_markup=edit_location_keyboard(location.id, page),
    )
    await delete_last_message(bot, state, message)


@router.message(F.text.as_("answer"), LocationState.editing, LocationStateOwner())
async def edit_location_field_entered(
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
