from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery

from bot.callbacks import GetTravelData, OpenMenu, Paginator
from bot.filters import TravelCallbackAccess
from bot.keyboards import one_travel_keyboard, travels_keyboard
from bot.utils.enums import BotMenu, SlashCommand
from bot.utils.format import format_travel
from core.models import TravelExtended
from core.services import TravelService

from .phrases import YOUR_TRAVELS

router = Router(name=__name__)


@router.message(Command(SlashCommand.TRAVELS))
async def all_travels_message(
    message: CallbackQuery,
    travel_service: TravelService,
) -> None:
    text = YOUR_TRAVELS
    keyboard = await travels_keyboard(message.from_user.id, 0, travel_service)
    await message.answer(text=text, reply_markup=keyboard)


@router.callback_query(OpenMenu.filter(F.menu == BotMenu.TRAVELS))
async def all_travels_callback(
    callback: CallbackQuery,
    travel_service: TravelService,
) -> None:
    text = YOUR_TRAVELS
    keyboard = await travels_keyboard(callback.from_user.id, 0, travel_service)
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(Paginator.filter(F.menu == BotMenu.TRAVELS))
async def paginate_travels(
    callback: CallbackQuery,
    callback_data: Paginator,
    travel_service: TravelService,
) -> None:
    text = YOUR_TRAVELS
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
