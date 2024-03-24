from aiogram import Router
from aiogram.types import CallbackQuery

from bot.callbacks import GetWeatherData
from bot.filters import LocationCallbackAccess
from bot.keyboards import back_to_location_keyboard
from bot.utils.format import format_weather
from core.models import LocationExtended
from core.services import WeatherService

router = Router(name=__name__)


@router.callback_query(GetWeatherData.filter(), LocationCallbackAccess())
async def get_weather(
    callback: CallbackQuery,
    callback_data: GetWeatherData,
    weather_service: WeatherService,
    location: LocationExtended,
) -> None:
    current, future = await weather_service.get_weather(location.city)
    text = format_weather(location.city, current, future)
    keyboard = back_to_location_keyboard(
        callback_data.location_id, location.travel_id, callback_data.page
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)
