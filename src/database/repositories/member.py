from sqlalchemy import ScalarSelect, delete, or_, select

from core.models import User, UserExtended
from core.repositories.member import MemberRepo
from database.models import (
    CityModel,
    LocationModel,
    TravelModel,
    UserModel,
    UsersToTravels,
)
from database.repositories.base import BaseAlchemyRepo

RECOMMENDED_TRAVELER_AGE_DIFFERENCE = 5


class MemberAlchemyRepo(MemberRepo, BaseAlchemyRepo):
    async def list_by_travel_id(
        self,
        travel_id: int,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[User]:
        query = (
            select(UserModel)
            .where(
                UserModel.id.in_(
                    select(UsersToTravels.member_id).where(
                        UsersToTravels.travel_id == travel_id
                    )
                )
            )
            .order_by(UserModel.name)
            .offset(offset)
        )
        if limit is not None:
            query = query.limit(limit)

        models = await self.session.scalars(query)
        return [User.model_validate(model) for model in models]

    async def add_to_travel(self, member_id: int, travel_id: int) -> None:
        relation = UsersToTravels(member_id=member_id, travel_id=travel_id)
        await self.session.merge(relation)
        await self.session.commit()

    async def remove_from_travel(self, member_id: int, travel_id: int) -> None:
        query = delete(UsersToTravels).where(
            UsersToTravels.member_id == member_id,  # но он работает .-.
            UsersToTravels.travel_id == travel_id,
        )
        await self.session.execute(query)
        await self.session.commit()

    async def recommended_travelers(
        self,
        travel_id: int,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[UserExtended]:
        def owner_query_field(field: str) -> ScalarSelect:
            return (
                select(getattr(UserModel, field))
                .where(
                    UserModel.id
                    == select(TravelModel.owner_id)
                    .where(TravelModel.id == travel_id)
                    .scalar_subquery()
                )
                .scalar_subquery()
            )

        age_difference = UserModel.age.between(
            owner_query_field("age") - RECOMMENDED_TRAVELER_AGE_DIFFERENCE,
            owner_query_field("age") + RECOMMENDED_TRAVELER_AGE_DIFFERENCE,
        )
        not_in_travel = UserModel.id.notin_(
            select(UsersToTravels.member_id).where(
                UsersToTravels.travel_id == travel_id
            )
        )
        in_owner_city_or_in_locations_city = or_(
            UserModel.city_id == owner_query_field("city_id"),
            UserModel.city_id.in_(
                select(CityModel.id).where(
                    CityModel.id.in_(
                        select(LocationModel.city_id).where(
                            LocationModel.travel_id == travel_id
                        )
                    )
                )
            ),
        )

        query = (
            select(UserModel)
            .where(age_difference, not_in_travel, in_owner_city_or_in_locations_city)
            .offset(offset)
        )
        if limit is not None:
            query = query.limit(limit)

        models = await self.session.scalars(query)
        return [UserExtended.model_validate(model) for model in models]
