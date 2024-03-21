from typing import cast

from sqlalchemy import select

from core.models import Country, CountryExtended
from core.repositories import CountryRepo
from database.models import CountryModel
from database.repositories.base import BaseAlchemyRepo


class CountryAlchemyRepo(CountryRepo, BaseAlchemyRepo):
    async def create(self, instance: Country) -> CountryExtended:
        country = await self.get_by_title(instance.title)
        if country:
            return country

        model = CountryModel(**instance.model_dump())
        self.session.add(model)
        await self.session.commit()
        return cast(CountryExtended, await self.get(model.id))

    async def get(self, id: int) -> CountryExtended | None:
        query = select(CountryModel).where(CountryModel.id == id)
        return await self.session.scalar(query)

    async def get_by_title(self, title: str) -> CountryExtended | None:
        query = select(CountryModel).where(CountryModel.title == title)
        model = await self.session.scalar(query)
        return CountryExtended.model_validate(model) if model else None

    async def get_by_alpha2(self, alpha2: str) -> CountryExtended | None:
        query = select(CountryModel).where(CountryModel.alpha2 == alpha2)
        model = await self.session.scalar(query)
        return CountryExtended.model_validate(model) if model else None
