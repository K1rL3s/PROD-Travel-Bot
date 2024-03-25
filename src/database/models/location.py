from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.location import MAX_LOCATION_ADDRESS_LENGTH, MAX_LOCATION_TITLE_LENGTH
from database.models.base import AlchemyBaseModel

if TYPE_CHECKING:
    from database.models.city import CityModel
    from database.models.country import CountryModel
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
    country_id: Mapped[int] = mapped_column(
        ForeignKey("countries.id"),
        nullable=False,
    )
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(MAX_LOCATION_TITLE_LENGTH),
        nullable=False,
    )
    address: Mapped[str] = mapped_column(
        String(MAX_LOCATION_ADDRESS_LENGTH),
        nullable=False,
    )
    start_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    travel: Mapped["TravelModel"] = relationship(
        "TravelModel",
        lazy="joined",
        cascade="save-update, merge, delete",
    )
    country: Mapped["CountryModel"] = relationship(
        "CountryModel",
        lazy="joined",
        cascade="save-update, merge, delete",
    )
    city: Mapped["CityModel"] = relationship(
        "CityModel",
        lazy="joined",
        cascade="save-update, merge, delete",
    )
