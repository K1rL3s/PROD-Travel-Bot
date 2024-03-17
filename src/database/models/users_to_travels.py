from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import AlchemyBaseModel

if TYPE_CHECKING:
    from database.models import TravelModel, UserModel


class UsersToTravels(AlchemyBaseModel):
    __tablename__ = "users_to_travels"

    member_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    travel_id: Mapped[int] = mapped_column(
        ForeignKey("travels.id"),
        primary_key=True,
    )

    member: Mapped["UserModel"] = relationship(
        "UserModel",
        cascade="save-update, merge, delete",
    )
    travel: Mapped["TravelModel"] = relationship(
        "TravelModel",
        cascade="save-update, merge, delete",
    )
