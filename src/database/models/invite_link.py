import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import AlchemyBaseModel

if TYPE_CHECKING:
    from database.models.travel import TravelModel


class InviteLinkModel(AlchemyBaseModel):
    __tablename__ = "invite_links"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    travel_id: Mapped[int] = mapped_column(ForeignKey("travels.id"), nullable=False)

    travel: Mapped["TravelModel"] = relationship(
        "TravelModel",
        cascade="save-update, merge, delete",
        lazy="joined",
    )
