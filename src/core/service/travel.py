from typing import Awaitable, Callable, TypeVar

from core.models import Travel
from core.models.travel import (
    MAX_TRAVEL_DESCRIPTION_LENGTH,
    MAX_TRAVEL_TITLE_LENGTH,
    TravelExtended,
)
from core.repositories import TravelRepo
from core.utils.enums import TravelField

T = TypeVar("T")


class TravelService:
    def __init__(self, travel_repo: TravelRepo) -> None:
        self.travel_repo = travel_repo

    async def is_owner(self, tg_id: int, travel_id: int) -> bool:
        return await self.travel_repo.is_owner(tg_id, travel_id)

    async def list_by_tg_id(
        self,
        tg_id: int,
    ) -> list[TravelExtended]:
        return await self.travel_repo.list_by_tg_id(tg_id=tg_id)

    async def get_with_access_check(
        self,
        tg_id: int,
        travel_id: int,
    ) -> TravelExtended | None:
        if not await self.travel_repo.is_has_access(tg_id, travel_id):
            return None

        return await self.travel_repo.get(travel_id)

    async def update_with_access_check(
        self,
        tg_id: int,
        travel_id: int,
        travel: Travel | TravelExtended,
    ) -> TravelExtended | None:
        if not await self.travel_repo.is_has_access(tg_id, travel_id):
            return None

        return await self.travel_repo.update(travel_id, travel)

    async def delete_with_access_check(
        self,
        tg_id: int,
        travel_id: int,
    ) -> None:
        if not await self.travel_repo.is_has_access(tg_id, travel_id):
            return None

        await self.travel_repo.delete(travel_id)

    async def create(self, travel: Travel) -> TravelExtended:
        return await self.travel_repo.create(travel)


# Да, оно будет браковать изменение названия своего путешествия на такое же
async def _validate_title(travel_service: TravelService, title: str) -> str | None:
    if (
        0 < len(title) <= MAX_TRAVEL_TITLE_LENGTH
        and await travel_service.travel_repo.get_by_title(title) is None
    ):
        return title


async def _validate_description(_, description: str) -> str | None:
    if 0 < len(description) <= MAX_TRAVEL_DESCRIPTION_LENGTH:
        return description


def get_travel_field_validator(
    field: str,
) -> Callable[[TravelService, T], Awaitable[T | None]]:
    if field == TravelField.TITLE:
        return _validate_title
    if field == TravelField.DESCRIPTION:
        return _validate_description
    raise ValueError("Unknown field")
