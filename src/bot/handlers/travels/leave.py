from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.callbacks import LeaveTravelData
from bot.filters import TravelCallbackAccess
from bot.handlers.travels.phrases import (
    YOU_CANT_LEAVE,
    YOUR_TRAVELS,
    ARE_YOU_SURE_LEAVE_TRAVEl,
)
from bot.keyboards.travels import leave_travel_keyboard, travels_keyboard
from core.models import TravelExtended
from core.services import MemberService, TravelService

router = Router(name=__name__)


@router.callback_query(
    LeaveTravelData.filter(F.sure.is_(False)),
    TravelCallbackAccess(),
)
async def leave_travel(
    callback: CallbackQuery,
    callback_data: LeaveTravelData,
    travel: TravelExtended,
) -> None:
    if callback.from_user.id == travel.owner_id:
        text = YOU_CANT_LEAVE
        keyboard = None
    else:
        text = ARE_YOU_SURE_LEAVE_TRAVEl.format(title=travel.title)
        keyboard = leave_travel_keyboard(callback_data.travel_id, callback_data.page)

    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(
    LeaveTravelData.filter(F.sure.is_(True)),
    TravelCallbackAccess(),
)
async def leave_travel_sure(
    callback: CallbackQuery,
    callback_data: LeaveTravelData,
    travel_service: TravelService,
    member_service: MemberService,
    travel: TravelExtended,
) -> None:
    if callback.from_user.id == travel.owner_id:
        text = YOU_CANT_LEAVE
        keyboard = None
    else:
        await member_service.self_leave(callback.from_user.id, callback_data.travel_id)
        text = YOUR_TRAVELS
        keyboard = await travels_keyboard(
            callback.message.from_user.id,
            callback_data.page,
            travel_service,
        )

    await callback.message.edit_text(text=text, reply_markup=keyboard)
