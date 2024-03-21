from abc import ABC, abstractmethod
from typing import Any, NoReturn

from core.models import City, CityExtended
from core.repositories.abc_meta import RepoMeta


class CityRepo(RepoMeta[City, CityExtended, int], ABC):
    async def delete(self, id: Any) -> NoReturn:
        raise TypeError("Cant delete city")

    async def update(self, id: Any, instance: Any) -> NoReturn:
        raise TypeError("Cand update city")

    @abstractmethod
    async def get_by_city_and_country(
        self,
        city: str,
        country: str,
    ) -> CityExtended | None:
        pass

    @abstractmethod
    async def get_by_city_and_country_id(
        self,
        city: str,
        country_id: int,
    ) -> CityExtended | None:
        pass
