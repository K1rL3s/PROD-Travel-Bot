from sqlalchemy import delete, select

from core.models import User
from core.repositories import UserRepo
from database.models import UserModel
from database.repositories.base import BaseAlchemyRepo


class UserAlchemyRepo(UserRepo, BaseAlchemyRepo):
    async def create(self, instance: User) -> User:
        location = UserModel(**instance.model_dump())
        self.session.add(location)
        await self.session.commit()
        return User.model_validate(location)

    async def delete(self, id: int) -> None:
        query = delete(UserModel).where(UserModel.id == id)
        await self.session.execute(query)
        await self.session.commit()

    async def get(self, id: int) -> User | None:
        query = select(UserModel).where(UserModel.id == id)
        model = await self.session.scalar(query)
        return User.model_validate(model) if model else None

    async def list(self, limit: int, offset: int) -> list[User]:
        query = select(UserModel).limit(limit).offset(offset)
        return [
            User.model_validate(model) for model in await self.session.scalars(query)
        ]

    async def update(self, id: int, instance: User) -> User:
        instance.id = id
        model = UserModel(**instance.model_dump())
        await self.session.merge(model)
        await self.session.commit()
        return User.model_validate(model)
