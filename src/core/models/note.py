from pydantic import Field

from core.models.base import BaseCoreModel
from core.models.travel import Travel
from core.models.user import User

MAX_NOTE_FILE_ID_LENGTH = 128
MAX_NOTE_TITLE_LENGTH = 64


class Note(BaseCoreModel):
    id: int | None = None
    title: str
    travel_id: int
    creator_id: int
    is_public: bool
    document_id: str = Field(max_length=MAX_NOTE_FILE_ID_LENGTH)


class NoteExtended(Note):
    id: int
    travel: Travel
    creator: User
