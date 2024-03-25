import datetime as dt
from typing import Any

from aiohttp import ClientSession

from core.geo import GeoWeather
from core.models import Weather

WEATHER_NOW_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
OK_STATUS = 200
SECONDS_IN_HOUR = 60 * 60


class OpenWeather(GeoWeather):
    def __init__(self, session: ClientSession, api_key: str) -> None:
        self.session = session
        self.api_key = api_key

    async def weather_now(self, latitude: float, longitude: float) -> Weather | None:
        params = {
            "lat": latitude,
            "lon": longitude,
            "units": "metric",
            "lang": "ru",
            "appid": self.api_key,
        }
        async with self.session.get(WEATHER_NOW_URL, params=params) as resp:
            if resp.status != OK_STATUS:
                return None
            return api_dict_to_weather_model(await resp.json())

    async def forecast(
        self,
        latitude: float,
        longitude: float,
        datetime: dt.datetime,
    ) -> Weather | None:
        datetime = (datetime - datetime.utcoffset()).replace(tzinfo=None)
        time_now = dt.datetime.utcnow()
        days_delta = (datetime - time_now).days
        hours_delta = min(
            5 * 24.0 - 1,  # 5 суток и минус для индекса
            (datetime - time_now).total_seconds() / SECONDS_IN_HOUR,
        )
        if days_delta < 0 or days_delta > 5:
            return None

        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": self.api_key,
            "lang": "ru",
            "units": "metric",
        }
        async with self.session.get(FORECAST_URL, params=params) as resp:
            if resp.status != OK_STATUS:
                return None
            forecast = await resp.json()
            return api_dict_to_weather_model(forecast["list"][int(hours_delta / 3)])


def api_dict_to_weather_model(result: dict[str, Any]) -> Weather:
    return Weather(
        temp=result["main"]["temp"],
        temp_min=result["main"]["temp_min"],
        temp_max=result["main"]["temp_max"],
        pressure=result["main"]["pressure"],
        humidity=result["main"]["humidity"],
        visibility=result["visibility"],
        wind_speed=result["wind"]["speed"],
        description=result["weather"][0]["description"],
        feels_like=result["main"]["feels_like"],
    )
