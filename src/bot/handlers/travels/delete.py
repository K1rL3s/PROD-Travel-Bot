from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callbacks import DeleteTravelData
from bot.filters import TravelCallbackOwner
from bot.keyboards import delete_travel_keyboard, travels_keyboard
from core.models import TravelExtended
from core.services import TravelService

from .phrases import YOUR_TRAVELS, ARE_YOU_SURE_DELETE_TRAVEl

router = Router(name=__name__)


@router.callback_query(
    DeleteTravelData.filter(F.sure.is_(False)),
    TravelCallbackOwner(),
)
async def delete_travel(
    callback: CallbackQuery,
    callback_data: DeleteTravelData,
    travel: TravelExtended,
) -> None:
    text = ARE_YOU_SURE_DELETE_TRAVEl.format(title=travel.title)
    keyboard = delete_travel_keyboard(callback_data.travel_id, callback_data.page)
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(
    DeleteTravelData.filter(F.sure.is_(True)),
    TravelCallbackOwner(),
)
async def delete_travel_sure(
    callback: CallbackQuery,
    callback_data: DeleteTravelData,
    state: FSMContext,
    travel: TravelExtended,
    travel_service: TravelService,
) -> None:
    await travel_service.delete_with_access_check(callback.from_user.id, travel.id)

    text = YOUR_TRAVELS
    keyboard = await travels_keyboard(
        callback.from_user.id,
        callback_data.page,
        travel_service,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)

    await state.clear()
