from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.models.user import (
    MAX_USER_CITY_LENGTH,
    MAX_USER_COUNTRY_LENGTH,
    MAX_USER_DESCRIPTION_LENGTH,
    MAX_USER_NAME_LENGTH,
)
from database.models.base import AlchemyBaseModel


class UserModel(AlchemyBaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        unique=True,
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(MAX_USER_NAME_LENGTH), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    country: Mapped[str] = mapped_column(
        String(MAX_USER_COUNTRY_LENGTH),
        nullable=False,
    )
    city: Mapped[str] = mapped_column(
        String(MAX_USER_CITY_LENGTH),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        String(MAX_USER_DESCRIPTION_LENGTH),
        nullable=True,
    )
