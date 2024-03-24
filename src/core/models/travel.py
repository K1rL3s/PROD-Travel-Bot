from pydantic import Field

from core.models.base import BaseCoreModel
from core.models.user import UserExtended

MAX_TRAVEL_TITLE_LENGTH = 256
MAX_TRAVEL_DESCRIPTION_LENGTH = 1024


class Travel(BaseCoreModel):
    id: int | None = None
    owner_id: int
    title: str = Field(min_length=1, max_length=MAX_TRAVEL_TITLE_LENGTH)
    description: str = Field(min_length=1, max_length=MAX_TRAVEL_DESCRIPTION_LENGTH)


class TravelExtended(Travel):
    id: int
    owner: UserExtended
