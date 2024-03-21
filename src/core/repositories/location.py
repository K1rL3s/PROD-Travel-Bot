from abc import ABC, abstractmethod

from core.models import Location, LocationExtended
from core.repositories.abc_meta import RepoMeta


class LocationRepo(RepoMeta[Location, LocationExtended, int], ABC):
    @abstractmethod
    async def list_by_travel_id(
        self,
        travel_id: int,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[LocationExtended]:
        pass
