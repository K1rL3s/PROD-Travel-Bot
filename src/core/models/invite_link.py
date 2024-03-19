from uuid import UUID

from pydantic import Field

from core.models.base import BasePydanticModel
from core.models.travel import Travel

INVITE_LINK_ID_LENGTH = 36
INVITE_LINK_ID_REGEX = (
    r"^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}$"
)


class InviteLink(BasePydanticModel):
    id: UUID | None = Field(None)
    travel_id: int


class InviteLinkExtended(InviteLink):
    travel: Travel
