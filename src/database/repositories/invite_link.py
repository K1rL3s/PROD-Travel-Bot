from uuid import UUID

from sqlalchemy import delete, select

from core.models import InviteLink, InviteLinkExtended
from core.repositories import InviteLinkRepo
from database.models import InviteLinkModel
from database.repositories.base import BaseAlchemyRepo


class InviteLinkAlchemyRepo(InviteLinkRepo, BaseAlchemyRepo):
    async def create(self, instance: InviteLink) -> InviteLinkExtended:
        link = InviteLinkModel(**instance.model_dump())
        self.session.add(link)
        await self.session.commit()
        return InviteLinkExtended.model_validate(await self.get(link.id))

    async def delete(self, id: UUID) -> None:
        query = delete(InviteLinkModel).where(InviteLinkModel.id == id)
        await self.session.execute(query)
        await self.session.commit()

    async def get(self, id: UUID) -> InviteLinkExtended | None:
        query = select(InviteLinkModel).where(InviteLinkModel.id == id)
        model = await self.session.scalar(query)
        return InviteLinkExtended.model_validate(model) if model else None
