from abc import ABC, abstractmethod
from typing import Any

from core.geo.location import GeoLocation


class GeoLocator(ABC):
    @abstractmethod
    async def geocode(
        self,
        query: dict | str,
        *,
        exactly_one: bool = True,
        timeout: int = 5,
        limit: int = None,
        addressdetails: bool = False,
        language: str = False,
        geometry: str = None,
        extratags: bool = False,
        country_codes: str | list[str] = None,
        viewbox: Any = None,
        bounded: bool = False,
        featuretype: str = None,
        namedetails: bool = False
    ) -> GeoLocation | list[GeoLocation] | None:
        pass
