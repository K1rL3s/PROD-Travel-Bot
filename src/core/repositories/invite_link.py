from abc import ABC
from typing import Any, NoReturn
from uuid import UUID

from core.models import InviteLink, InviteLinkExtended
from core.repositories.abc import RepoMeta


class InviteLinkRepo(RepoMeta[InviteLink, InviteLinkExtended, UUID], ABC):
    async def update(self, id: Any, instance: Any) -> NoReturn:
        return TypeError("Cant update invite link")
