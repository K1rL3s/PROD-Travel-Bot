from sqlalchemy import delete, select

from core.models import Travel
from core.repositories import TravelRepo
from database.models import TravelModel
from database.repositories.base import BaseAlchemyRepo


class TravelAlchemyRepo(TravelRepo, BaseAlchemyRepo):
    async def create(self, instance: Travel) -> Travel:
        location = TravelModel(**instance.model_dump())
        self.session.add(location)
        await self.session.commit()
        return Travel.model_validate(location)

    async def delete(self, id: int) -> None:
        query = delete(TravelModel).where(TravelModel.id == id)
        await self.session.execute(query)
        await self.session.commit()

    async def get(self, id: int) -> Travel | None:
        query = select(TravelModel).where(TravelModel.id == id)
        model = await self.session.scalar(query)
        return Travel.model_validate(model) if model else None

    async def list(self, limit: int, offset: int) -> list[Travel]:
        query = select(TravelModel).limit(limit).offset(offset)
        return [
            Travel.model_validate(model) for model in await self.session.scalars(query)
        ]

    async def update(self, id: int, instance: Travel) -> Travel:
        instance.id = id
        model = TravelModel(**instance.model_dump())
        await self.session.merge(model)
        await self.session.commit()
        return Travel.model_validate(model)
