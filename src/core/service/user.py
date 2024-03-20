from typing import Awaitable, Callable

from core.models import User
from core.models.user import (
    MAX_USER_CITY_LENGTH,
    MAX_USER_COUNTRY_LENGTH,
    MAX_USER_DESCRIPTION_LENGTH,
    MAX_USER_NAME_LENGTH,
)
from core.repositories import UserRepo
from core.utils.enums import ProfileField


class UserService:
    def __init__(self, user_repo: UserRepo) -> None:
        self.user_repo = user_repo

    async def get(self, tg_id: int) -> User | None:
        return await self.user_repo.get(tg_id)

    async def create(self, instance: User) -> User:
        return await self.user_repo.create(instance)

    async def update(self, tg_id: int, instance: User) -> User:
        return await self.user_repo.update(tg_id, instance)

    @staticmethod
    async def validate_name(_, name: str) -> bool:
        return 0 < len(name) <= MAX_USER_NAME_LENGTH

    @staticmethod
    async def validate_age(_, age: str) -> bool:
        return isinstance(age, str) and age.isdigit() and 0 < int(age) < 125

    @staticmethod
    async def validate_city(_, city: str) -> bool:
        return 0 < len(city) <= MAX_USER_CITY_LENGTH

    @staticmethod
    async def validate_country(_, country: str) -> bool:
        return 0 < len(country) <= MAX_USER_COUNTRY_LENGTH

    @staticmethod
    async def validate_description(_, description: str) -> bool:
        return 0 < len(description) <= MAX_USER_DESCRIPTION_LENGTH


def get_user_field_validator(
    field: str,
) -> Callable[[UserService, str], Awaitable[bool]]:
    if field == ProfileField.NAME:
        return UserService.validate_name
    if field == ProfileField.AGE:
        return UserService.validate_age
    if field == ProfileField.CITY:
        return UserService.validate_city
    if field == ProfileField.COUNTRY:
        return UserService.validate_country
    if field == ProfileField.DESCRIPTION:
        return UserService.validate_description
    raise ValueError("Unknown field")
