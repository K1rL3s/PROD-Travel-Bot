from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from core.models import Location, Note, Travel, User

# Тайпвар модели
M = TypeVar("M")
# Тайпвар айдишника
K = TypeVar("K")


class RepoMeta(ABC, Generic[M, K]):
    @abstractmethod
    async def create(self, instance: M) -> M:
        pass

    @abstractmethod
    async def delete(self, id: K) -> None:
        pass

    @abstractmethod
    async def get(self, id: K) -> M | None:
        pass

    @abstractmethod
    async def update(self, id: K, instance: M) -> M:
        pass


class LocationRepo(RepoMeta[Location, int], ABC):
    pass


class NoteRepo(RepoMeta[Note, int], ABC):
    pass


class TravelRepo(RepoMeta[Travel, int], ABC):
    @abstractmethod
    async def get_by_title(self, title: str) -> Travel | None:
        pass

    @abstractmethod
    async def list_by_tg_id(self, tg_id: int, limit: int, offset: int) -> list[Travel]:
        pass

    @abstractmethod
    async def is_has_access(self, tg_id: int, travel_id: int) -> bool:
        pass


class UserRepo(RepoMeta[User, int], ABC):
    pass
