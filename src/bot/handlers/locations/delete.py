from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callbacks.location import DeleteLocationData
from bot.filters.location import LocationCallbackOwner
from bot.keyboards.locations import delete_location_keyboard, locations_keyboard
from core.models import LocationExtended
from core.service.location import LocationService
from core.service.travel import TravelService

router = Router(name=__name__)


@router.callback_query(
    DeleteLocationData.filter(F.sure.is_(False)),
    LocationCallbackOwner(),
)
async def delete_location(
    callback: CallbackQuery,
    callback_data: DeleteLocationData,
    location: LocationExtended,
) -> None:
    text = f'Вы уверены, что хотите удалить локацию "{location.title}"?'
    keyboard = delete_location_keyboard(callback_data.location_id, callback_data.page)
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(
    DeleteLocationData.filter(F.sure.is_(True)),
    LocationCallbackOwner(),
)
async def delete_location_sure(
    callback: CallbackQuery,
    callback_data: DeleteLocationData,
    state: FSMContext,
    location: LocationExtended,
    location_service: LocationService,
    travel_service: TravelService,
) -> None:
    await location_service.delete_with_access_check(callback.from_user.id, location.id)

    text = "Локации"
    keyboard = await locations_keyboard(
        callback.from_user.id,
        callback_data.page,
        location.travel_id,
        location_service,
        travel_service,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)

    await state.clear()