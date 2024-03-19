from sqlalchemy import delete, select

from core.models import User
from core.repositories.member import MemberRepo
from database.models import UserModel, UsersToTravels
from database.repositories.base import BaseAlchemyRepo


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
            UsersToTravels.member_id == member_id,
            UsersToTravels.travel_id == travel_id,
        )
        await self.session.execute(query)
        await self.session.commit()
