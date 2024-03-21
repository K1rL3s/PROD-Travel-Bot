from typing import cast

from sqlalchemy import delete, select

from core.models import User, UserExtended
from core.repositories import UserRepo
from database.models import UserModel
from database.repositories.base import BaseAlchemyRepo


class UserAlchemyRepo(UserRepo, BaseAlchemyRepo):
    async def create(self, instance: User) -> UserExtended:
        user = UserModel(**instance.model_dump())
        self.session.add(user)
        await self.session.commit()

        model = cast(UserModel, await self.get(instance.id))
        return UserExtended.model_validate(model)

    async def delete(self, id: int) -> None:
        query = delete(UserModel).where(UserModel.id == id)
        await self.session.execute(query)
        await self.session.commit()

    async def get(self, id: int) -> UserExtended | None:
        query = select(UserModel).where(UserModel.id == id)
        model = await self.session.scalar(query)
        return UserExtended.model_validate(model) if model else None

    async def update(self, id: int, instance: User | UserExtended) -> UserExtended:
        instance.id = id
        model = UserModel(**instance.model_dump(exclude={"city", "country"}))
        await self.session.merge(model)
        await self.session.commit()

        model = cast(UserModel, await self.get(instance.id))
        return UserExtended.model_validate(model)
