from sqlalchemy import delete, select

from core.models import Note
from core.repositories import NoteRepo
from database.models import NoteModel
from database.repositories.base import BaseAlchemyRepo


class NoteAlchemyRepo(NoteRepo, BaseAlchemyRepo):
    async def create(self, instance: Note) -> Note:
        location = NoteModel(**instance.model_dump())
        self.session.add(location)
        await self.session.commit()
        return Note.model_validate(location)

    async def delete(self, id: int) -> None:
        query = delete(NoteModel).where(NoteModel.id == id)
        await self.session.execute(query)
        await self.session.commit()

    async def get(self, id: int) -> Note | None:
        query = select(NoteModel).where(NoteModel.id == id)
        model = await self.session.scalar(query)
        return Note.model_validate(model) if model else None

    async def update(self, id: int, instance: Note) -> Note:
        instance.id = id
        model = NoteModel(**instance.model_dump())
        await self.session.merge(model)
        await self.session.commit()
        return Note.model_validate(model)
