from pydantic import Field

from core.models.base import BasePydanticModel
from core.models.travel import Travel

MAX_NOTE_FILE_ID_LENGTH = 128


class Note(BasePydanticModel):
    id: int | None = Field(None)
    travel_id: int
    is_public: bool
    file_id: str = Field(max_length=MAX_NOTE_FILE_ID_LENGTH)


class NoteExtended(Note):
    id: int
    travel: Travel
