from core.models import Note, NoteExtended
from core.repositories import NoteRepo, TravelRepo


class NoteService:
    def __init__(self, note_repo: NoteRepo, travel_repo: TravelRepo) -> None:
        self.note_repo = note_repo
        self.travel_repo = travel_repo

    async def is_has_access_to_check_note(self, tg_id: int, note_id: int) -> bool:
        note = await self.note_repo.get(note_id)
        if note is None:
            return False
        if (
            not await self.travel_repo.is_has_access(tg_id, note.travel_id)
            or tg_id != note.travel.owner_id
        ):
            return False
        return True

    async def get_with_access_check(
        self,
        tg_id: int,
        note_id: int,
    ) -> NoteExtended | None:
        if await self.is_has_access_to_check_note(tg_id, note_id):
            return await self.note_repo.get(note_id)
        return None

    async def create_with_access_check(
        self,
        tg_id: int,
        note: Note,
    ) -> NoteExtended | None:
        if not self.travel_repo.is_has_access(tg_id, note.travel_id):
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
