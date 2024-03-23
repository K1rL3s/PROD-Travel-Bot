from abc import ABC, abstractmethod
from typing import Any, NoReturn

from core.models import User, UserExtended
from core.repositories.abc_meta import RepoMeta


class MemberRepo(RepoMeta[User, User, int], ABC):
    @abstractmethod
    async def list_by_travel_id(
        self,
        travel_id: int,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[User]:
        pass

    @abstractmethod
    async def add_to_travel(
        self,
        member_id: int,
        travel_id: int,
    ) -> None:
        pass

    @abstractmethod
    async def remove_from_travel(
        self,
        member_id: int,
        travel_id: int,
    ) -> None:
        pass

    @abstractmethod
    async def recommended_travelers(
        self,
        travel_id: int,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[UserExtended]:
        pass

    async def create(self, instance: Any) -> NoReturn:
        raise TypeError(
            "Use `UserRepo` for creating users or `.add` for inviting to travels"
        )

    async def delete(self, id: Any) -> NoReturn:
        raise TypeError("Use `.remove` to delete user from travel")

    async def get(self, id: Any) -> NoReturn:
        raise TypeError("Use `.list_by_travel_id()` to get members")

    async def update(self, id: Any, instance: Any) -> NoReturn:
        raise TypeError("There is no update in MemberRepo")
