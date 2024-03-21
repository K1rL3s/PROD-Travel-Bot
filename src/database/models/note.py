from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.note import MAX_NOTE_FILE_ID_LENGTH, MAX_NOTE_TITLE_LENGTH
from database.models.base import AlchemyBaseModel

if TYPE_CHECKING:
    from database.models.travel import TravelModel
    from database.models.user import UserModel


class NoteModel(AlchemyBaseModel):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False,
    )
    travel_id: Mapped[int] = mapped_column(ForeignKey("travels.id"), nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False)
    title: Mapped[str] = mapped_column(String(MAX_NOTE_TITLE_LENGTH), nullable=False)
    document_id: Mapped[str] = mapped_column(
        String(MAX_NOTE_FILE_ID_LENGTH),
        nullable=False,
    )

    travel: Mapped["TravelModel"] = relationship(
        "TravelModel",
        cascade="save-update, merge, delete",
        lazy="joined",
    )
    creator: Mapped["UserModel"] = relationship(
        "UserModel",
        cascade="save-update, merge, delete",
        lazy="joined",
    )
