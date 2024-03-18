from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import TYPE_CHECKING

from core.models.note import MAX_NOTE_FILE_ID_LENGTH
from database.models.base import AlchemyBaseModel

if TYPE_CHECKING:
    from database.models import TravelModel


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
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False)
    file_id: Mapped[str] = mapped_column(
        String(MAX_NOTE_FILE_ID_LENGTH),
        nullable=False,
    )

    travel: Mapped["TravelModel"] = relationship(
        "TravelModel",
        cascade="save-update, merge, delete",
        lazy="joined",
    )
