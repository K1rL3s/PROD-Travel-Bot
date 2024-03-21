from abc import ABC, abstractmethod

from core.models import Note, NoteExtended
from core.repositories.abc_meta import RepoMeta


class NoteRepo(RepoMeta[Note, NoteExtended, int], ABC):
    @abstractmethod
    async def list(
        self,
        tg_id: int,
        travel_id: int,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[NoteExtended]:
        pass
