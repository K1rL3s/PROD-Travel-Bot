from sqlalchemy import delete, select

from core.models import Location
from core.repositories import LocationRepo
from database.models import LocationModel
from database.repositories.base import BaseAlchemyRepo


class LocationAlchemyRepo(LocationRepo, BaseAlchemyRepo):
    async def create(self, instance: Location) -> Location:
        location = LocationModel(**instance.model_dump())
        self.session.add(location)
        await self.session.commit()
        return Location.model_validate(location)

    async def delete(self, id: int) -> None:
        query = delete(LocationModel).where(LocationModel.id == id)
        await self.session.execute(query)
        await self.session.commit()

    async def get(self, id: int) -> Location | None:
        query = select(LocationModel).where(LocationModel.id == id)
        model = await self.session.scalar(query)
        return Location.model_validate(model) if model else None

    async def update(self, id: int, instance: Location) -> Location:
        instance.id = id
        model = LocationModel(**instance.model_dump())
        await self.session.merge(model)
        await self.session.commit()
        return Location.model_validate(model)
