from sqlalchemy import delete, or_, select

from core.models import Travel
from core.repositories import TravelRepo
from database.models import TravelModel, UsersToTravels
from database.repositories.base import BaseAlchemyRepo


class TravelAlchemyRepo(TravelRepo, BaseAlchemyRepo):
    async def create(self, instance: Travel) -> Travel:
        travel = TravelModel(**instance.model_dump())
        self.session.add(travel)
        await self.session.flush()

        relation = UsersToTravels(travel_id=travel.id, member_id=instance.owner_id)
        self.session.add(relation)

        await self.session.commit()
        return Travel.model_validate(travel)

    async def delete(self, id: int) -> None:
        relations_query = delete(UsersToTravels).where(UsersToTravels.travel_id == id)
        await self.session.execute(relations_query)
        await self.session.flush()

        travel_query = delete(TravelModel).where(TravelModel.id == id)
        await self.session.execute(travel_query)
        await self.session.commit()

    async def get(self, id: int) -> Travel | None:
        query = select(TravelModel).where(TravelModel.id == id)
        model = await self.session.scalar(query)
        return Travel.model_validate(model) if model else None

    async def get_by_title(self, title: str) -> Travel | None:
        query = select(TravelModel).where(TravelModel.title == title)
        model = await self.session.scalar(query)
        return Travel.model_validate(model) if model else None

    async def update(self, id: int, instance: Travel) -> Travel:
        instance.id = id
        model = TravelModel(**instance.model_dump())
        await self.session.merge(model)
        await self.session.commit()
        return Travel.model_validate(model)

    async def list_by_tg_id(self, tg_id: int, limit: int, offset: int) -> list[Travel]:
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
        )
        models = await self.session.scalars(query)
        return [Travel.model_validate(model) for model in models]

    async def is_has_access(self, tg_id: int, travel_id: int) -> bool:
        query = select(UsersToTravels).where(
            UsersToTravels.travel_id == travel_id,
            UsersToTravels.member_id == tg_id,
        )
        return bool(await self.session.scalar(query))
