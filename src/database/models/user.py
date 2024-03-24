from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.user import (
    MAX_TG_NAME_LENGTH,
    MAX_USER_DESCRIPTION_LENGTH,
    MAX_USER_NAME_LENGTH,
)
from database.models.base import AlchemyBaseModel

if TYPE_CHECKING:
    from database.models.city import CityModel
    from database.models.country import CountryModel


class UserModel(AlchemyBaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        unique=True,
        nullable=False,
    )
    country_id: Mapped[int] = mapped_column(
        ForeignKey("countries.id"),
        nullable=False,
    )
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String(MAX_USER_NAME_LENGTH), nullable=False)
    tg_username: Mapped[str | None] = mapped_column(
        String(MAX_TG_NAME_LENGTH),
        nullable=True,
    )
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(
        String(MAX_USER_DESCRIPTION_LENGTH),
        nullable=True,
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
