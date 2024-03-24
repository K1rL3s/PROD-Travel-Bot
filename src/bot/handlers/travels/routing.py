from aiogram import Router
from aiogram.types import CallbackQuery

from bot.callbacks import GetRouteData
from bot.filters import TravelCallbackAccess
from bot.keyboards import back_to_travel_keyboard
from core.models import TravelExtended
from core.services import LocationService, RoutingService

from .phrases import NOT_ENOUGH_LOCATIONS, ROUTE_URL

router = Router(name=__name__)


@router.callback_query(GetRouteData.filter(), TravelCallbackAccess())
async def get_route(
    callback: CallbackQuery,
    callback_data: GetRouteData,
    routing_service: RoutingService,
    location_service: LocationService,
    travel: TravelExtended,
) -> None:
    locations = await location_service.list_by_travel_id_with_access_check(
        callback.from_user.id,
        callback_data.travel_id,
    )
    if locations:
        text = ROUTE_URL.format(url=await routing_service.get_route_url(travel))
    else:
        text = NOT_ENOUGH_LOCATIONS
    keyboard = back_to_travel_keyboard(callback_data.travel_id, callback_data.page)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
