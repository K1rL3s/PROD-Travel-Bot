from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import TYPE_CHECKING

from core.models.location import (
    MAX_LOCATION_ADDRESS_LENGTH,
    MAX_LOCATION_CITY_LENGTH,
    MAX_LOCATION_COUNTRY_LENGTH,
    MAX_LOCATION_TITLE_LENGTH,
)
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
    title: Mapped[str] = mapped_column(
        String(MAX_LOCATION_TITLE_LENGTH),
        nullable=False,
    )
    country: Mapped[str] = mapped_column(
        String(MAX_LOCATION_COUNTRY_LENGTH),
        nullable=False,
    )
    city: Mapped[str] = mapped_column(
        String(MAX_LOCATION_CITY_LENGTH),
        nullable=False,
    )
    address: Mapped[str] = mapped_column(
        String(MAX_LOCATION_ADDRESS_LENGTH),
        nullable=False,
    )
    start_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    end_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    travel: Mapped["TravelModel"] = relationship(
        "TravelModel",
        lazy="joined",
        cascade="save-update, merge, delete",
    )
