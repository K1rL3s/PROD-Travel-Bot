from typing import cast

from sqlalchemy import delete, or_, select

from core.models import Note, NoteExtended
from core.repositories import NoteRepo
from database.models import NoteModel, TravelModel
from database.repositories.base import BaseAlchemyRepo


class NoteAlchemyRepo(NoteRepo, BaseAlchemyRepo):
    async def create(self, instance: Note) -> NoteExtended:
        note = NoteModel(**instance.model_dump())
        self.session.add(note)
        await self.session.commit()

        model = cast(NoteModel, await self.get(note.id))
        return NoteExtended.model_validate(model)

    async def delete(self, id: int) -> None:
        query = delete(NoteModel).where(NoteModel.id == id)
        await self.session.execute(query)
        await self.session.commit()

    async def get(self, id: int) -> NoteExtended | None:
        query = select(NoteModel).where(NoteModel.id == id)
        model = await self.session.scalar(query)
        return NoteExtended.model_validate(model) if model else None

    async def update(self, id: int, instance: Note | NoteExtended) -> NoteExtended:
        instance.id = id
        model = NoteModel(**instance.model_dump(exclude={"travel", "creator"}))
        await self.session.merge(model)
        await self.session.commit()

        new_model = cast(NoteModel, await self.get(id))
        return NoteExtended.model_validate(new_model)

    async def list(
        self,
        tg_id: int,
        travel_id: int,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[NoteExtended]:
        query = (
            select(NoteModel)
            .where(
                NoteModel.travel_id == travel_id,
                or_(
                    NoteModel.is_public,
                    NoteModel.creator_id == tg_id,
                    tg_id
                    == select(TravelModel.owner_id)
                    .where(TravelModel.id == travel_id)
                    .subquery(),
                ),
            )
            .offset(offset)
            .order_by(NoteModel.id.desc())
        )
        if limit is not None:
            query = query.limit(limit)

        models = await self.session.scalars(query)
        return [NoteExtended.model_validate(model) for model in models]
