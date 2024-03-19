from uuid import UUID

from core.models import InviteLink, InviteLinkExtended, TravelExtended, User
from core.repositories import InviteLinkRepo, TravelRepo
from core.repositories.member import MemberRepo
from core.service.base import BaseService


class MemberService(BaseService):
    def __init__(
        self,
        member_repo: MemberRepo,
        travel_repo: TravelRepo,
        invite_link_repo: InviteLinkRepo,
    ) -> None:
        self.member_repo = member_repo
        self.travel_repo = travel_repo
        self.invite_link_repo = invite_link_repo

    async def list_with_access_check(self, tg_id: int, travel_id: int) -> list[User]:
        if not await self.travel_repo.is_has_access(tg_id, travel_id):
            return []

        return await self.member_repo.list_by_travel_id(travel_id)

    async def delete_with_access_check(
        self,
        tg_id: int,
        member_id: int,
        travel_id: int,
    ) -> None:
        if not await self.travel_repo.is_owner(tg_id, travel_id):
            return None

        await self.member_repo.remove_from_travel(member_id, travel_id)

    async def use_invite_link(
        self,
        tg_id: int,
        invite_id: UUID,
    ) -> TravelExtended | None:
        invite_link = await self.invite_link_repo.get(invite_id)
        if invite_link is None:
            return None

        await self.member_repo.add_to_travel(tg_id, invite_link.travel_id)
        await self.invite_link_repo.delete(invite_link.id)

        travel = await self.travel_repo.get(invite_link.travel_id)
        return TravelExtended.model_validate(travel)

    async def create_invite_link_with_access_check(
        self,
        tg_id: int,
        travel_id: int,
    ) -> InviteLinkExtended | None:
        if not await self.travel_repo.is_owner(tg_id, travel_id):
            return None

        return await self.invite_link_repo.create(InviteLink(travel_id=travel_id))
