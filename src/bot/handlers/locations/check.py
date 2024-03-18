from aiogram import Router
from aiogram.types import CallbackQuery

from bot.callbacks.location import GetLocationData, LocationPaginator
from bot.filters.location_access import LocationCallbackAccess
from bot.filters.travel_access import TravelCallbackAccess
from bot.handlers.locations.funcs import format_location
from bot.keyboards.locations import locations_keyboard, one_location_keyboard
from core.models import LocationExtended, TravelExtended
from core.service.location import LocationService
from core.service.travel import TravelService

router = Router(name=__name__)


@router.callback_query(LocationPaginator.filter(), TravelCallbackAccess())
async def paginate_locations(
    callback: CallbackQuery,
    callback_data: LocationPaginator,
    travel: TravelExtended,
    location_service: LocationService,
    travel_service: TravelService,
) -> None:
    text = f'Локации путешествия "{travel.title}"'
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
