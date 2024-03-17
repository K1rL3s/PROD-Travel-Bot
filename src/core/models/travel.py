from core.models.base import BasePydanticModel


class Travel(BasePydanticModel):
    id: int | None = None
    owner_id: int
    title: str
    description: str
