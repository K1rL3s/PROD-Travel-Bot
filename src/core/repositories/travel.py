from abc import ABC, abstractmethod

from core.models import Travel, TravelExtended
from core.repositories.abc_meta import RepoMeta


class TravelRepo(RepoMeta[Travel, TravelExtended, int], ABC):
    @abstractmethod
    async def get_by_title_and_owner_id(
        self,
        title: str,
        owner_id: int,
    ) -> TravelExtended | None:
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

    @abstractmethod
    async def is_owner(self, tg_id: int, travel_id: int) -> bool:
        pass
