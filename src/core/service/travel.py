from typing import Awaitable, Callable

from core.models import Travel
from core.repositories.abc import TravelRepo


class TravelService:
    def __init__(self, travel_repo: TravelRepo) -> None:
        self.travel_repo = travel_repo

    async def list_by_tg_id(
        self,
        tg_id: int,
        page: int,
        objs_per_page: int = 6,
    ) -> list[Travel]:
        return await self.travel_repo.list_by_tg_id(
            tg_id=tg_id,
            limit=objs_per_page,
            offset=page * objs_per_page,
        )

    async def create(self, travel: Travel) -> Travel:
        return await self.travel_repo.create(travel)

    async def get_with_access_check(self, tg_id: int, travel_id: int) -> Travel | None:
        if not await self.travel_repo.is_has_access(tg_id, travel_id):
            return None

        return await self.travel_repo.get(travel_id)

    async def update_with_access_check(
        self,
        tg_id: int,
        travel_id: int,
        travel: Travel,
    ) -> Travel | None:
        if not await self.travel_repo.is_has_access(tg_id, travel_id):
            return None

        return await self.travel_repo.update(travel_id, travel)

    async def delete_with_access_check(
        self,
        tg_id: int,
        travel_id: int,
    ) -> Travel | None:
        if not await self.travel_repo.is_has_access(tg_id, travel_id):
            return None

        return await self.travel_repo.delete(travel_id)


# Да, оно будет браковать изменение названия своего путешествия на такое же
async def _validate_title(travel_service: TravelService, title: str) -> bool:
    return (
        0 < len(title) <= 256
        and await travel_service.travel_repo.get_by_title(title) is None
    )


async def _validate_description(_, description: str) -> bool:
    return 0 < len(description) <= 1024


def get_travel_field_validator(
    field: str,
) -> Callable[[TravelService, str], Awaitable[bool]]:
    if field == "title":
        return _validate_title
    if field == "description":
        return _validate_description
    raise ValueError("Unknown field")
