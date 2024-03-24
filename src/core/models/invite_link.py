from uuid import UUID

from core.models.base import BaseCoreModel
from core.models.travel import Travel

INVITE_LINK_ID_LENGTH = 36
INVITE_LINK_ID_REGEX = (
    r"^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}$"
)


class InviteLink(BaseCoreModel):
    id: UUID | None = None
    travel_id: int


class InviteLinkExtended(InviteLink):
    id: UUID
    travel: Travel
