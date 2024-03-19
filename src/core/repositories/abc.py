from abc import ABC, abstractmethod
from typing import Generic, TypeVar

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
