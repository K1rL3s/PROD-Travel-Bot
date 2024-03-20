from typing import Any, cast

from core.geo import GeoLocation, GeoLocator
from core.service.base import BaseService


class GeoService(BaseService):
    def __init__(self, geolocator: GeoLocator) -> None:
        self.geolocator = geolocator
        self.kwargs = {
            "language": "ru",
            "addressdetails": True,
            "extratags": True,
        }

    async def geocode(
        self,
        query: str,
        **kwargs: Any,
    ) -> GeoLocation | list[GeoLocation] | None:
        if kwargs:
            options = self.kwargs.copy()
            options.update(kwargs)
        else:
            options = self.kwargs
        return await self.geolocator.geocode(query, **options)

    async def normalize_city(self, city: str) -> str | None:
        location = cast(
            GeoLocation,
            await self.geocode(city, featuretype="city", exactly_one=True),
        )
        if not location:
            return None

        return location.raw.get("address", {}).get("city")

    async def normalize_country(self, country: str) -> str | None:
        location = cast(
            GeoLocation,
            await self.geocode(country, featuretype="country"),
        )
        if not location:
            return None

        return location.raw.get("address", {}).get("country")

    async def get_countries_by_city(self, city: str) -> list[str]:
        locations = cast(
            list[GeoLocation],
            await self.geocode(city, featuretype="city", exactly_one=False, limit=10),
        )
        if not locations:
            return []

        return sorted(
            {
                location.raw["address"]["country"]
                for location in locations
                if location.raw.get("address", {}).get("country")
            }
        )

    async def get_address(self, title: str, city: str, country: str) -> str | None:
        location = cast(GeoLocation, await self.geocode(f"{title} {city} {country}"))
        if not location:
            return None

        return location.address
