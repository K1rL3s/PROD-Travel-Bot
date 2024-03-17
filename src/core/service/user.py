from typing import Callable

from core.models import User
from core.repositories import UserRepo


class UserService:
    def __init__(self, user_repo: UserRepo) -> None:
        self.user_repo = user_repo

    async def get(self, tg_id: int) -> User:
        return await self.user_repo.get(tg_id)

    async def create(self, instance: User) -> User:
        return await self.user_repo.create(instance)

    async def update(self, tg_id: int, instance: User) -> User:
        return await self.user_repo.update(tg_id, instance)

    @staticmethod
    def validate_name(name: str) -> bool:
        return 0 < len(name) < 128

    @staticmethod
    def validate_age(age: str) -> bool:
        return isinstance(age, str) and age.isdigit() and 0 < int(age) < 125

    @staticmethod
    def validate_country(country: str) -> bool:
        return 0 < len(country) < 128

    @staticmethod
    def validate_city(city: str) -> bool:
        return 0 < len(city) < 128

    @staticmethod
    def validate_description(description: str) -> bool:
        return 0 < len(description) < 256


def get_user_field_validator(field: str) -> Callable[[str], bool]:
    if field == "name":
        return UserService.validate_name
    if field == "age":
        return UserService.validate_age
    if field == "city":
        return UserService.validate_city
    if field == "description":
        return UserService.validate_description
    raise ValueError("Unknown field")
