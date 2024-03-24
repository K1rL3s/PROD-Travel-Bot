from typing import cast

from sqlalchemy import delete, or_, select

from core.models import Travel, TravelExtended
from core.repositories import TravelRepo
from database.models import (
    InviteLinkModel,
    LocationModel,
    NoteModel,
    TravelModel,
    UsersToTravels,
)
from database.repositories.base import BaseAlchemyRepo


class TravelAlchemyRepo(TravelRepo, BaseAlchemyRepo):
    async def create(self, instance: Travel) -> TravelExtended:
        travel = TravelModel(**instance.model_dump())
        self.session.add(travel)
        await self.session.flush()

        relation = UsersToTravels(travel_id=travel.id, member_id=instance.owner_id)
        self.session.add(relation)
        await self.session.commit()

        new_travel = await self.get(travel.id)
        return TravelExtended.model_validate(new_travel)

    async def delete(self, id: int) -> None:
        members_query = delete(UsersToTravels).where(UsersToTravels.travel_id == id)
        locations_query = delete(LocationModel).where(LocationModel.travel_id == id)
        notes_query = delete(NoteModel).where(NoteModel.travel_id == id)
        links_query = delete(InviteLinkModel).where(InviteLinkModel.travel_id == id)
        await self.session.execute(members_query)
        await self.session.execute(locations_query)
        await self.session.execute(notes_query)
        await self.session.execute(links_query)
        await self.session.flush()

        travel_query = delete(TravelModel).where(TravelModel.id == id)
        await self.session.execute(travel_query)
        await self.session.commit()

    async def get(self, id: int) -> TravelExtended | None:
        query = select(TravelModel).where(TravelModel.id == id)
        model = await self.session.scalar(query)
        return TravelExtended.model_validate(model) if model else None

    async def get_by_title_and_owner_id(
        self,
        title: str,
        owner_id: int,
    ) -> TravelExtended | None:
        query = select(TravelModel).where(
            TravelModel.title == title,
            TravelModel.owner_id == owner_id,
        )
        model = await self.session.scalar(query)
        return TravelExtended.model_validate(model) if model else None

    async def update(
        self,
        id: int,
        instance: Travel | TravelExtended,
    ) -> TravelExtended:
        instance.id = id
        model = TravelModel(**instance.model_dump(exclude={"owner"}))
        await self.session.merge(model)
        await self.session.commit()

        model = cast(TravelModel, await self.get(id))
        return TravelExtended.model_validate(model)

    async def list_by_tg_id(
        self,
        tg_id: int,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[TravelExtended]:
        query = (
            select(TravelModel)
            .where(
                or_(
                    TravelModel.owner_id == tg_id,
                    TravelModel.id.in_(
                        select(UsersToTravels.travel_id).where(
                            UsersToTravels.member_id == tg_id
                        )
                    ),
                )
            )
            .order_by(TravelModel.title)
            .offset(offset)
        )
        if limit is not None:
            query = query.limit(limit)

        models = await self.session.scalars(query)
        return [TravelExtended.model_validate(model) for model in models]

    async def is_has_access(self, tg_id: int, travel_id: int) -> bool:
        query = select(UsersToTravels).where(
            UsersToTravels.travel_id == travel_id,
            UsersToTravels.member_id == tg_id,
        )
        return bool(await self.session.scalar(query))

    async def is_owner(self, tg_id: int, travel_id: int) -> bool:
        query = select(TravelModel).where(
            TravelModel.id == travel_id,
            TravelModel.owner_id == tg_id,
        )
        return bool(await self.session.scalar(query))
