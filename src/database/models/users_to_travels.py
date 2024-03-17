from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import AlchemyBaseModel


class UsersToTravels(AlchemyBaseModel):
    __tablename__ = "users_to_travels"

    member_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    travel_id: Mapped[int] = mapped_column(ForeignKey("travels.id"), primary_key=True)
