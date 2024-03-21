from abc import ABC, abstractmethod
from typing import Any, NoReturn

from core.models import Country, CountryExtended
from core.repositories.abc_meta import RepoMeta


class CountryRepo(RepoMeta[Country, CountryExtended, int], ABC):
    async def delete(self, id: Any) -> NoReturn:
        raise TypeError("Cant delete country")

    async def update(self, id: Any, instance: Any) -> NoReturn:
        raise TypeError("Cand update country")

    @abstractmethod
    async def get_by_title(self, title: str) -> CountryExtended | None:
        pass

    @abstractmethod
    async def get_by_alpha2(self, alpha2: str) -> CountryExtended | None:
        pass
