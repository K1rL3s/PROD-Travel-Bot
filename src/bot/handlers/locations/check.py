from aiogram import Router
from aiogram.types import CallbackQuery

from bot.callbacks import GetLocationData, LocationsPaginator
from bot.filters import LocationCallbackAccess, TravelCallbackAccess
from bot.keyboards import locations_keyboard, one_location_keyboard
from bot.utils.format import format_location
from core.models import LocationExtended, TravelExtended
from core.services import LocationService, TravelService

from .phrases import ALL_LOCATIONS

router = Router(name=__name__)


@router.callback_query(LocationsPaginator.filter(), TravelCallbackAccess())
async def paginate_locations(
    callback: CallbackQuery,
    callback_data: LocationsPaginator,
    travel: TravelExtended,
    location_service: LocationService,
    travel_service: TravelService,
) -> None:
    text = ALL_LOCATIONS.format(title=travel.title)
    keyboard = await locations_keyboard(
        callback.from_user.id,
        callback_data.page,
        travel.id,
        location_service,
        travel_service,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(
    GetLocationData.filter(),
    LocationCallbackAccess(),
)
async def one_travel(
    callback: CallbackQuery,
    callback_data: GetLocationData,
    location: LocationExtended,
) -> None:
    text = format_location(location)
    keyboard = one_location_keyboard(
        location,
        callback.from_user.id,
        callback_data.page,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)
