from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.city import MAX_CITY_LENGTH, MAX_TIMEZONE_LENGTH
from database.models.base import AlchemyBaseModel

if TYPE_CHECKING:
    from database.models import CountryModel


class CityModel(AlchemyBaseModel):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False,
    )
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"), nullable=False)

    title: Mapped[str] = mapped_column(String(MAX_CITY_LENGTH), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    timezone: Mapped[str] = mapped_column(String(MAX_TIMEZONE_LENGTH), nullable=False)

    country: Mapped["CountryModel"] = relationship(
        "CountryModel",
        lazy="joined",
        cascade="save-update, merge, delete",
    )
