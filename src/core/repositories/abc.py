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
    async def list(self, limit: int, offset: int) -> list[M]:
        pass

    @abstractmethod
    async def update(self, id: K, instance: M) -> M:
        pass


class LocationRepo(RepoMeta[Location, int], ABC):
    pass


class NoteRepo(RepoMeta[Note, int], ABC):
    pass


class TravelRepo(RepoMeta[Travel, int], ABC):
    pass


class UserRepo(RepoMeta[User, int], ABC):
    pass
