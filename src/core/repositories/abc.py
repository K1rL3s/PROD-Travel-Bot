from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from core.models import (
    Location,
    LocationExtended,
    Note,
    NoteExtended,
    Travel,
    TravelExtended,
    User,
)

# Тайпвар core модели
M = TypeVar("M")
# Тайпвар extended core модели
ExtM = TypeVar("ExtM")
# Тайпвар айдишника
K = TypeVar("K")


class RepoMeta(ABC, Generic[M, ExtM, K]):
    @abstractmethod
    async def create(self, instance: M) -> ExtM:
        pass

    @abstractmethod
    async def delete(self, id: K) -> None:
        pass

    @abstractmethod
    async def get(self, id: K) -> ExtM | None:
        pass

    @abstractmethod
    async def update(self, id: K, instance: M) -> ExtM:
        pass


class TravelRepo(RepoMeta[Travel, TravelExtended, int], ABC):
    @abstractmethod
    async def get_by_title(self, title: str) -> TravelExtended | None:
        pass

    @abstractmethod
    async def list_by_tg_id(
        self,
        tg_id: int,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[TravelExtended]:
        pass

    @abstractmethod
    async def is_has_access(self, tg_id: int, travel_id: int) -> bool:
        pass


class LocationRepo(RepoMeta[Location, LocationExtended, int], ABC):
    @abstractmethod
    async def list_by_travel_id(
        self,
        travel_id: int,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[LocationExtended]:
        pass


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


class UserRepo(RepoMeta[User, User, int], ABC):
    pass
