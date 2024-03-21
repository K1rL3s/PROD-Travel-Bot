from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import AlchemyBaseModel


class CountryModel(AlchemyBaseModel):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    alpha2: Mapped[str] = mapped_column(String(2), nullable=False, unique=True)
