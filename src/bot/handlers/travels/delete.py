from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callbacks.travel import DeleteTravelData, TravelCRUD
from bot.filters.travel_access import TravelCallbackAccess
from bot.keyboards.travels import delete_travel_keyboard, travels_keyboard
from bot.utils.enums import Action
from core.models import Travel
from core.service.travel import TravelService

router = Router(name=__name__)


@router.callback_query(
    TravelCRUD.filter(F.action == Action.DELETE),
    TravelCallbackAccess(),
)
async def delete_travel(
    callback: CallbackQuery,
    callback_data: TravelCRUD,
    travel: Travel,
) -> None:
    text = f'Вы уверены, что хотите удалить путешествие под названием "{travel.title}"?'
    keyboard = delete_travel_keyboard(callback_data.id, callback_data.page)
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(
    DeleteTravelData.filter(),
    TravelCallbackAccess(),
)
async def delete_travel_sure(
    callback: CallbackQuery,
    callback_data: DeleteTravelData,
    state: FSMContext,
    travel: Travel,
    travel_service: TravelService,
) -> None:
    await travel_service.delete_with_access_check(callback.from_user.id, travel.id)

    text = "Ваши путешествия"
    keyboard = await travels_keyboard(
        callback.from_user.id,
        callback_data.page,
        travel_service,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)

    await state.clear()
