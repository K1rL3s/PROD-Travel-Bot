from typing import Awaitable, Callable, TypeVar

from core.models import Note, NoteExtended
from core.models.note import MAX_NOTE_TITLE_LENGTH
from core.repositories import NoteRepo, TravelRepo
from core.utils.enums import NoteField

T = TypeVar("T")


class NoteService:
    def __init__(self, note_repo: NoteRepo, travel_repo: TravelRepo) -> None:
        self.note_repo = note_repo
        self.travel_repo = travel_repo

    async def is_has_access_to_check(self, tg_id: int, note_id: int) -> bool:
        note = await self.note_repo.get(note_id)
        if note is None:
            return False
        if (
            not await self.travel_repo.is_has_access(tg_id, note.travel_id)
            or tg_id != note.travel.owner_id
        ):
            return False
        return True

    async def is_owner(self, tg_id: int, note_id: int) -> bool:
        note = await self.note_repo.get(note_id)
        if note is None:
            return False
        return tg_id == note.creator_id or tg_id == note.travel.owner_id

    async def get_with_access_check(
        self,
        tg_id: int,
        note_id: int,
    ) -> NoteExtended | None:
        if await self.is_has_access_to_check(tg_id, note_id):
            return await self.note_repo.get(note_id)
        return None

    async def create_with_access_check(
        self,
        tg_id: int,
        note: Note,
    ) -> NoteExtended | None:
        if not await self.travel_repo.is_has_access(tg_id, note.travel_id):
            return None

        return await self.note_repo.create(note)

    async def list_with_access_check(
        self,
        tg_id: int,
        travel_id: int,
    ) -> list[NoteExtended]:
        if not await self.travel_repo.is_has_access(tg_id, travel_id):
            return []

        return await self.note_repo.list(tg_id, travel_id)

    async def delete_with_access_check(self, tg_id: int, note_id: int) -> None:
        if not await self.is_owner(tg_id, note_id):
            return None

        await self.note_repo.delete(note_id)

    async def switch_status_with_access_check(
        self,
        tg_id: int,
        note_id: int,
    ) -> NoteExtended | None:
        if not await self.is_owner(tg_id, note_id):
            return None

        note = await self.note_repo.get(note_id)
        if note is None:
            return None

        note.is_public = not note.is_public
        instanse = Note(**note.model_dump(exclude={"creator", "travel"}))

        await self.note_repo.update(note.id, instanse)

        return note

    @staticmethod
    async def validate_title(_: "NoteService", title: str) -> str | None:
        if 0 < len(title) <= MAX_NOTE_TITLE_LENGTH:
            return title
        return None


def get_location_field_validator(
    field: str,
) -> Callable[[NoteService, T], Awaitable[T | None]]:
    if field == NoteField.TITLE:
        return NoteService.validate_title
    raise ValueError("Unknown field")
