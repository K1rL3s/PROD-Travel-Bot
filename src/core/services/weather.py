import asyncio
import datetime as dt

import pytz

from core.geo import GeoWeather
from core.models import City, Weather
from core.services.base import BaseService


class WeatherService(BaseService):
    def __init__(self, geo_weather: GeoWeather) -> None:
        self.geo_weather = geo_weather

    async def get_weather(self, city: City) -> tuple[Weather | None, Weather | None]:
        city_tz = pytz.timezone(city.timezone)
        city_time = dt.datetime.now(tz=city_tz)
        forecast_datetime = city_time + dt.timedelta(days=5)
        now, after = await asyncio.gather(
            self.geo_weather.weather_now(city.latitude, city.longitude),
            self.geo_weather.forecast(city.latitude, city.longitude, forecast_datetime),
        )
        return now, after
