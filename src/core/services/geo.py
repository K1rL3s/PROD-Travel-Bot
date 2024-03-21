from typing import Any, cast

from core.geo import GeoLocation, GeoLocator
from core.models import City, CityExtended, Country, CountryExtended
from core.repositories import CityRepo, CountryRepo
from core.services.base import BaseService


class GeoService(BaseService):
    def __init__(
        self,
        geolocator: GeoLocator,
        country_repo: CountryRepo,
        city_repo: CityRepo,
    ) -> None:
        self.geolocator = geolocator
        self.country_repo = country_repo
        self.city_repo = city_repo
        self.geo_kwargs = {
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
            options = self.geo_kwargs.copy()
            options.update(kwargs)
        else:
            options = self.geo_kwargs
        return await self.geolocator.geocode(query, **options)

    async def normalize_city(self, city: str) -> str | None:
        location = cast(
            GeoLocation,
            await self.geocode(city, featuretype="city", exactly_one=True),
        )
        return location.local_title if location else None

    async def normalize_country(self, country: str) -> str | None:
        location = cast(
            GeoLocation,
            await self.geocode(country, featuretype="country", exactly_one=True),
        )
        return location.country_title if location else None

    async def create_or_get_city(self, city: str, country: str) -> CityExtended | None:
        if existed := await self.city_repo.get_by_city_and_country(city, country):
            return existed

        location = cast(
            GeoLocation,
            await self.geocode(
                f"{city} {country}",
                featuretype="city",
                exactly_one=True,
            ),
        )
        if location is None:
            return None
        if location.local_title is None:
            return None
        if location.country_title is None:
            return None

        country = await self.create_or_get_country(location.country_title)
        if country is None:
            return None

        city = City(
            title=location.local_title,
            country_id=country.id,
            latitude=location.latitude,
            longitude=location.longitude,
        )
        return await self.city_repo.create(city)

    async def create_or_get_country(self, country: str) -> CountryExtended | None:
        if existed := await self.country_repo.get_by_title(country):
            return existed

        location = cast(
            GeoLocation,
            await self.geocode(country, featuretype="country", exactly_one=True),
        )
        if location is None:
            return None
        if location.country_title is None:
            return None

        country = Country(title=location.country_title, alpha2=location.country_code)
        return await self.country_repo.create(country)

    async def get_countries_by_city(self, city: str) -> list[str]:
        locations = cast(
            list[GeoLocation],
            await self.geocode(city, featuretype="city", exactly_one=False, limit=10),
        )
        if not locations:
            return []

        return sorted(
            {location.country_title for location in locations if location.country_title}
        )

    async def get_address(self, title: str, city: str, country: str) -> str | None:
        location = cast(GeoLocation, await self.geocode(f"{title} {city} {country}"))
        if not location:
            return None

        return location.address