import datetime as dt
from abc import ABC, abstractmethod
from typing import Any


class GeoWeather(ABC):
    @abstractmethod
    async def weather_now(
        self,
        latitude: float,
        longitude: float,
    ) -> dict[str, Any] | None:
        pass

    @abstractmethod
    async def forecast(
        self,
        latitude: float,
        longitude: float,
        datetime: dt.datetime,
    ) -> dict[str, Any] | None:
        pass
