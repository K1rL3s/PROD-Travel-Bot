from abc import ABC, abstractmethod
from typing import Any

from core.geo.location import GeoLocation
from core.geo.point import GeoPoint


class GeoLocator(ABC):
    @abstractmethod
    async def geocode(
        self,
        query: dict | str,
        *,
        exactly_one: bool = True,
        timeout: float = 5.0,
        limit: int = None,
        addressdetails: bool = False,
        language: str = False,
        geometry: str = None,
        extratags: bool = False,
        country_codes: str | list[str] = None,
        viewbox: Any = None,
        bounded: bool = False,
        featuretype: str = None,
        namedetails: bool = False,
    ) -> GeoLocation | list[GeoLocation] | None:
        pass

    @abstractmethod
    async def reverse(
        self,
        query: str | tuple[float, float] | GeoPoint,
        *,
        exactly_one: bool = True,
        timeout: float = 5.0,
        language: str = False,
        addressdetails: bool = True,
        zoom: int = None,
        namedetails: bool = False,
    ) -> GeoLocation | list[GeoLocation] | None:
        pass
