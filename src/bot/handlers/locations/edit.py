from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.location import EditLocationData
from bot.filters.location_access import LocationCallbackOwner, LocationStateOwner
from bot.keyboards.locations import edit_location_keyboard
from bot.keyboards.universal import back_cancel_keyboard
from bot.utils.html import html_quote
from bot.utils.states import LocationState
from bot.utils.tg import delete_last_message
from core.models import LocationExtended, User
from core.service.location import LocationService, get_location_field_validator
from core.utils.enums import LocationField

from .funcs import format_location
from .phrases import error_text_by_field

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


@router.message(F.text, LocationState.editing, LocationStateOwner())
async def edit_location_field_enter(
    message: Message,
    bot: Bot,
    state: FSMContext,
    user: User,
    location: LocationExtended,
    location_service: LocationService,
) -> None:
    data = await state.get_data()
    edit_field: str = data["field"]
    page: int = data["page"]

    validator = get_location_field_validator(edit_field)
    error_text = error_text_by_field[edit_field]
    if (value := await validator(location_service, message.text)) is None:
        await message.reply(text=error_text, reply_markup=back_cancel_keyboard)
        await delete_last_message(bot, state, message)
        return

    setattr(location, edit_field, html_quote(value))
    await location_service.update_with_access_check(user.id, location.id, location)
    await message.answer(
        text=format_location(location),
        reply_markup=edit_location_keyboard(location.id, page),
    )
    await delete_last_message(bot, state, message)
