from core.models.base import BasePydanticModel


class Note(BasePydanticModel):
    id: int | None
    owner_id: int
    travel_id: int
    is_public: bool
    file_id: str
