from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import TYPE_CHECKING

from core.models.travel import MAX_TRAVEL_DESCRIPTION_LENGTH, MAX_TRAVEL_TITLE_LENGTH
from database.models.base import AlchemyBaseModel

if TYPE_CHECKING:
    from database.models.user import UserModel


class TravelModel(AlchemyBaseModel):
    __tablename__ = "travels"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False,
    )
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(
        String(MAX_TRAVEL_TITLE_LENGTH),
        nullable=False,
        unique=True,
    )
    description: Mapped[str] = mapped_column(
        String(MAX_TRAVEL_DESCRIPTION_LENGTH),
        nullable=False,
    )

    owner: Mapped[list["UserModel"]] = relationship(
        "UserModel",
        lazy="joined",
    )
