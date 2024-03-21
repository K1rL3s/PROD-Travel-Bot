from typing import Callable

from core.models import User
from core.models.city import MAX_CITY_LENGTH
from core.models.country import MAX_COUNTRY_LENGTH
from core.models.user import (
    MAX_USER_DESCRIPTION_LENGTH,
    MAX_USER_NAME_LENGTH,
    UserExtended,
)
from core.repositories import UserRepo
from core.utils.enums import ProfileField


class UserService:
    def __init__(self, user_repo: UserRepo) -> None:
        self.user_repo = user_repo

    async def get(self, tg_id: int) -> UserExtended | None:
        return await self.user_repo.get(tg_id)

    async def create(self, instance: User) -> UserExtended:
        return await self.user_repo.create(instance)

    async def update(self, tg_id: int, instance: User) -> UserExtended:
        return await self.user_repo.update(tg_id, instance)


def validate_name(name: str) -> bool:
    return 0 < len(name) <= MAX_USER_NAME_LENGTH


def validate_age(age: str) -> bool:
    return isinstance(age, str) and age.isdigit() and 0 < int(age) < 125


def validate_country(country: str) -> bool:
    return 0 < len(country) <= MAX_COUNTRY_LENGTH


def validate_city(city: str) -> bool:
    return 0 < len(city) <= MAX_CITY_LENGTH


def validate_description(description: str) -> bool:
    return 0 < len(description) <= MAX_USER_DESCRIPTION_LENGTH


def get_user_field_validator(
    field: str,
) -> Callable[[str], bool]:
    if field == ProfileField.NAME:
        return validate_name
    if field == ProfileField.AGE:
        return validate_age
    if field == ProfileField.CITY:
        return validate_city
    if field == ProfileField.COUNTRY:
        return validate_country
    if field == ProfileField.DESCRIPTION:
        return validate_description
    raise ValueError("Unknown field")
