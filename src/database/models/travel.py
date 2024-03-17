from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import TYPE_CHECKING

from database.models.base import AlchemyBaseModel

if TYPE_CHECKING:
    from database.models.location import LocationModel


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
    title: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(1024), nullable=False)

    locations: Mapped[list["LocationModel"]] = relationship(
        "LocationModel",
        back_populates="travel",
        lazy="selectin",
    )
