from typing import Any, Callable, Coroutine, TypeVar

from core.models import Location, LocationExtended
from core.models.location import (
    MAX_LOCATION_ADDRESS_LENGTH,
    MAX_LOCATION_CITY_LENGTH,
    MAX_LOCATION_COUNTRY_LENGTH,
    MAX_LOCATION_TITLE_LENGTH,
)
from core.repositories import LocationRepo, TravelRepo
from core.utils.enums import LocationField

T = TypeVar("T")


class LocationService:
    def __init__(self, location_repo: LocationRepo, travel_repo: TravelRepo) -> None:
        self.location_repo = location_repo
        self.travel_repo = travel_repo

    async def is_has_access(
        self,
        tg_id: int,
        location_id: int,
    ) -> bool:
        location = await self.location_repo.get(location_id)
        if location is None:
            return False

        return await self.travel_repo.is_has_access(tg_id, location.travel_id)

    async def is_owner(self, tg_id: int, location_id: int) -> bool:
        location = await self.get_with_access_check(tg_id, location_id)
        return location is not None and location.travel.owner_id == tg_id

    async def get_with_access_check(
        self,
        tg_id: int,
        location_id: int,
    ) -> LocationExtended | None:
        location = await self.location_repo.get(location_id)
        if location is None:
            return None
        if not await self.travel_repo.is_has_access(tg_id, location.travel_id):
            return None
        return location

    async def delete_with_access_check(self, tg_id: int, location_id: int) -> None:
        if not await self.is_owner(tg_id, location_id):
            return

        await self.location_repo.delete(location_id)

    async def update_with_access_check(
        self,
        tg_id: int,
        location_id: int,
        location: Location | LocationExtended,
    ) -> LocationExtended | None:
        if not await self.is_owner(tg_id, location_id):
            return None

        return await self.location_repo.update(location_id, location)

    async def list_by_travel_id_with_access_check(
        self,
        tg_id: int,
        travel_id: int,
    ) -> list[LocationExtended]:
        if not await self.travel_repo.is_has_access(tg_id, travel_id):
            return []

        return await self.location_repo.list_by_travel_id(travel_id=travel_id)

    async def create(self, location: Location) -> LocationExtended:
        return await self.location_repo.create(location)

    @staticmethod
    async def validate_title(_: "LocationService", title: str) -> str | None:
        if 0 < len(title) <= MAX_LOCATION_TITLE_LENGTH:
            return title
        return None

    @staticmethod
    async def validate_city(_: "LocationService", city: str) -> str | None:
        if 0 < len(city) <= MAX_LOCATION_CITY_LENGTH:
            return city
        return None

    @staticmethod
    async def validate_country(_: "LocationService", country: str) -> str | None:
        if 0 < len(country) <= MAX_LOCATION_COUNTRY_LENGTH:
            return country
        return None

    @staticmethod
    async def validate_address(_: "LocationService", address: str) -> str | None:
        if 0 < len(address) <= MAX_LOCATION_ADDRESS_LENGTH:
            return address
        return None

    @staticmethod
    async def validate_start_at(_: "LocationService", start_at: str) -> str | None:
        return start_at

    @staticmethod
    async def validate_end_at(_: "LocationService", end_at: str) -> str | None:
        return end_at


def get_location_field_validator(
    field: str,
) -> Callable[[LocationService, T], Coroutine[Any, Any, T | None]]:
    if field == LocationField.TITLE:
        return LocationService.validate_title
    if field == LocationField.CITY:
        return LocationService.validate_city
    if field == LocationField.COUNTRY:
        return LocationService.validate_country
    if field == LocationField.ADDRESS:
        return LocationService.validate_address
    if field == LocationField.START_AT:
        return LocationService.validate_start_at
    if field == LocationField.END_AT:
        return LocationService.validate_end_at
    raise ValueError("Unknown field")
