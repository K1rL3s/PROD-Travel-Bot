from typing import cast

from sqlalchemy import select

from core.models import City, CityExtended
from core.repositories import CityRepo
from database.models import CityModel, CountryModel
from database.repositories.base import BaseAlchemyRepo


class CityAlchemyRepo(CityRepo, BaseAlchemyRepo):
    async def create(self, instance: City) -> CityExtended:
        city = await self.get_by_city_and_country_id(
            instance.title,
            instance.country_id,
        )
        if city:
            return city

        model = CityModel(**instance.model_dump())
        self.session.add(model)
        await self.session.commit()
        return cast(CityExtended, await self.get(model.id))

    async def get(self, id: int) -> CityExtended | None:
        query = select(CityModel).where(CityModel.id == id)
        return await self.session.scalar(query)

    async def get_by_city_and_country(
        self,
        city: str,
        country: str,
    ) -> CityExtended | None:
        query = select(CityModel).where(
            CityModel.title == city,
            CityModel.country_id
            == select(CountryModel.id)
            .where(CountryModel.title == country)
            .scalar_subquery(),
        )
        model = await self.session.scalar(query)
        return CityExtended.model_validate(model) if model else None

    async def get_by_city_and_country_id(
        self,
        city: str,
        country_id: int,
    ) -> CityExtended | None:
        query = select(CityModel).where(
            CityModel.title == city,
            CityModel.country_id == country_id,
        )
        model = await self.session.scalar(query)
        return CityExtended.model_validate(model) if model else None
