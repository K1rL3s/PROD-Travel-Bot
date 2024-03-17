from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import TYPE_CHECKING

from database.models.base import AlchemyBaseModel

if TYPE_CHECKING:
    from database.models.travel import TravelModel


class LocationModel(AlchemyBaseModel):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False,
    )
    travel_id: Mapped[int] = mapped_column(ForeignKey("travels.id"), nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(1024), nullable=False)
    country: Mapped[str] = mapped_column(String(256), nullable=False)
    city: Mapped[str] = mapped_column(String(256), nullable=False)
    address: Mapped[str] = mapped_column(String(256), nullable=False)
    start_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    end_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    travel: Mapped["TravelModel"] = relationship(
        "TravelModel",
        back_populates="locations",
        lazy="selectin",
        cascade="save-update, merge, delete",
    )
