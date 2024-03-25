from aiogram import Router
from aiogram.types import BufferedInputFile, CallbackQuery

from bot.callbacks import GetRouteData
from bot.filters import TravelCallbackAccess
from bot.keyboards import back_to_travel_keyboard, one_travel_keyboard
from bot.utils.format import format_travel
from core.models import TravelExtended
from core.services import LocationService, RoutingService

from .phrases import BAD_ROUTE, NOT_ENOUGH_LOCATIONS, PROCESSING, ROUTE_URL

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
    if len(locations) < 1:
        text = NOT_ENOUGH_LOCATIONS
        keyboard = back_to_travel_keyboard(callback_data.travel_id, callback_data.page)
        await callback.message.answer(text=text, reply_markup=keyboard)
        return

    text = PROCESSING
    bot_msg = await callback.message.answer(text=text)

    url, file = await routing_service.get_route(travel)
    if file:
        caption = ROUTE_URL.format(url=url)
        image = BufferedInputFile(file=file, filename=f"route_{travel.id}")
        await callback.message.answer_photo(photo=image, caption=caption)
    else:
        text = BAD_ROUTE
        await callback.message.answer(text=text)

    text = format_travel(travel)
    keyboard = one_travel_keyboard(
        travel,
        callback.from_user.id,
        callback_data.page,
    )
    await callback.message.answer(text=text, reply_markup=keyboard)

    await bot_msg.delete()
