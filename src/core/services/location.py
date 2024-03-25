import datetime as dt
from typing import Callable, TypeVar

from bot.utils.datehelp import datetime_by_format
from core.models import Location, LocationExtended
from core.models.city import MAX_CITY_LENGTH
from core.models.country import MAX_COUNTRY_LENGTH
from core.models.location import MAX_LOCATION_ADDRESS_LENGTH, MAX_LOCATION_TITLE_LENGTH
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


def validate_title(title: str) -> bool:
    return 0 < len(title) <= MAX_LOCATION_TITLE_LENGTH


def validate_city(city: str) -> bool:
    return 0 < len(city) <= MAX_CITY_LENGTH


def validate_country(country: str) -> bool:
    return 0 < len(country) <= MAX_COUNTRY_LENGTH


def validate_address(address: str) -> bool:
    return 0 < len(address) <= MAX_LOCATION_ADDRESS_LENGTH


def validate_start_at(start_at: str) -> bool:
    return bool(datetime_by_format(start_at))


def validate_end_at(end_at: str, start_at: dt.datetime) -> bool:
    end = datetime_by_format(end_at)
    return end is not None and end >= start_at


def get_location_field_validator(
    field: str,
) -> Callable[[str], bool]:
    if field == LocationField.TITLE:
        return validate_title
    if field == LocationField.CITY:
        return validate_city
    if field == LocationField.COUNTRY:
        return validate_country
    if field == LocationField.ADDRESS:
        return validate_address
    raise ValueError("Wrong field")
