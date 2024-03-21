from typing import cast

from sqlalchemy import delete, select

from core.models import Location, LocationExtended
from core.repositories import LocationRepo
from database.models import LocationModel
from database.repositories.base import BaseAlchemyRepo


class LocationAlchemyRepo(LocationRepo, BaseAlchemyRepo):
    async def create(self, instance: Location) -> LocationExtended:
        location = LocationModel(**instance.model_dump())
        self.session.add(location)
        await self.session.commit()
        return LocationExtended.model_validate(await self.get(location.id))

    async def delete(self, id: int) -> None:
        query = delete(LocationModel).where(LocationModel.id == id)
        await self.session.execute(query)
        await self.session.commit()

    async def get(self, id: int) -> LocationExtended | None:
        query = select(LocationModel).where(LocationModel.id == id)
        model = await self.session.scalar(query)
        return LocationExtended.model_validate(model) if model else None

    async def update(
        self,
        id: int,
        instance: Location | LocationExtended,
    ) -> LocationExtended:
        instance.id = id
        model = LocationModel(
            **instance.model_dump(exclude={"travel", "city", "country"})
        )
        await self.session.merge(model)
        await self.session.commit()

        new_model = cast(LocationModel, await self.get(id))
        return LocationExtended.model_validate(new_model)

    async def list_by_travel_id(
        self,
        travel_id: int,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[LocationExtended]:
        query = (
            select(LocationModel)
            .where(LocationModel.travel_id == travel_id)
            .order_by(LocationModel.start_at)
            .offset(offset)
        )
        if limit is not None:
            query = query.limit(limit)

        models = await self.session.scalars(query)
        return [LocationExtended.model_validate(model) for model in models]
