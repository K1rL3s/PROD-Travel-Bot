from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.callbacks.menu import OpenMenu
from bot.callbacks.paginate import Paginator
from bot.callbacks.travels import GetTravelData
from bot.filters.travels import TravelCallbackAccess
from bot.handlers.travels.funcs import format_travel
from bot.keyboards.travels import one_travel_keyboard, travels_keyboard
from bot.utils.enums import BotMenu
from core.models import TravelExtended
from core.service.travel import TravelService

router = Router(name=__name__)


@router.callback_query(OpenMenu.filter(F.menu == BotMenu.TRAVELS))
async def all_travels(
    callback: CallbackQuery,
    travel_service: TravelService,
) -> None:
    text = "Ваши путешествия"
    keyboard = await travels_keyboard(callback.from_user.id, 0, travel_service)
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(Paginator.filter(F.menu == BotMenu.TRAVELS))
async def paginate_travels(
    callback: CallbackQuery,
    callback_data: Paginator,
    travel_service: TravelService,
) -> None:
    text = "Ваши путешествия"
    keyboard = await travels_keyboard(
        callback.from_user.id,
        callback_data.page,
        travel_service,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(
    GetTravelData.filter(),
    TravelCallbackAccess(),
)
async def one_travel(
    callback: CallbackQuery,
    callback_data: GetTravelData,
    travel: TravelExtended,
) -> None:
    text = format_travel(travel)
    keyboard = one_travel_keyboard(
        travel,
        callback.from_user.id,
        callback_data.page,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)
