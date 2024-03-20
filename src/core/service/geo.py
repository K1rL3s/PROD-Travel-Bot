from typing import cast

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

    async def normalize_city(self, city: str) -> str | None:
        location = cast(
            GeoLocation,
            await self.geolocator.geocode(
                city,
                **self.kwargs,
                featuretype="city",
                exactly_one=True,
            ),
        )
        if not location:
            return None

        if location.raw.get("address", {}).get("city"):
            return location.raw["address"]["city"]
        return None

    async def normalize_country(self, country: str) -> str | None:
        location = cast(
            GeoLocation,
            await self.geolocator.geocode(
                country,
                **self.kwargs,
                featuretype="country",
            ),
        )
        if not location:
            return None

        if location.raw.get("address", {}).get("country"):
            return location.raw["address"]["country"]
        return None

    async def get_countries_by_city(self, city: str) -> list[str]:
        locations = cast(
            list[GeoLocation],
            await self.geolocator.geocode(
                city,
                **self.kwargs,
                featuretype="city",
                exactly_one=False,
                limit=5,
            ),
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
