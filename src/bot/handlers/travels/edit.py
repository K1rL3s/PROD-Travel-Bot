from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.travel import EditTravelData, TravelCRUD
from bot.filters.travel_access import TravelCallbackAccess, TravelStateAccess
from bot.keyboards.travels import edit_travel_keyboard
from bot.keyboards.universal import back_cancel_keyboard
from bot.utils.enums import Action
from bot.utils.states import TravelState
from bot.utils.tg import delete_last_message
from core.models import Travel, User
from core.service.travel import TravelService, get_travel_field_validator
from core.utils.enums import TravelField

from .funcs import format_travel
from .phrases import error_text_by_field

router = Router(name=__name__)


@router.callback_query(
    TravelCRUD.filter(F.action == Action.EDIT), TravelCallbackAccess()
)
async def edit_travel(
    callback: CallbackQuery,
    callback_data: TravelCRUD,
    travel: Travel,
) -> None:
    text = "Что вы хотите изменить?\n\n" + format_travel(travel)
    keyboard = edit_travel_keyboard(callback_data.id, callback_data.page)
    await callback.message.edit_text(text=text, reply_markup=keyboard)


for field in TravelField.values():

    @router.callback_query(
        EditTravelData.filter(F.field == field), TravelCallbackAccess()
    )
    async def edit_travel_field(
        callback: CallbackQuery,
        callback_data: EditTravelData,
        state: FSMContext,
        travel: Travel,
    ) -> None:
        text = "Введите новое значение.\nТекущее: " + str(
            getattr(travel, callback_data.field)
        )
        await callback.message.edit_text(text=text, reply_markup=back_cancel_keyboard)
        await state.set_data(
            {
                "last_id": callback.message.message_id,
                "travel_id": callback_data.id,
                "field": callback_data.field,
                "page": callback_data.page,
            },
        )
        await state.set_state(TravelState.editing)


@router.message(F.text, TravelState.editing, TravelStateAccess())
async def edit_travel_field_enter(
    message: Message,
    bot: Bot,
    state: FSMContext,
    user: User,
    travel: Travel,
    travel_service: TravelService,
) -> None:
    data = await state.get_data()
    edit_field: str = data["field"]
    page: int = data["page"]

    validator = get_travel_field_validator(edit_field)
    error_text = error_text_by_field[edit_field]
    if not await validator(travel_service, message.text):
        await message.reply(text=error_text, reply_markup=back_cancel_keyboard)
        await delete_last_message(bot, state, message)
        return

    setattr(travel, edit_field, message.text)
    await travel_service.update_with_access_check(user.id, travel.id, travel)
    await message.answer(
        text=format_travel(travel),
        reply_markup=edit_travel_keyboard(travel.id, page),
    )
    await delete_last_message(bot, state, message)
