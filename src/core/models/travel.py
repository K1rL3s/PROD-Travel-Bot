from typing import TYPE_CHECKING

from core.models.base import BasePydanticModel

if TYPE_CHECKING:
    from core.models.location import Location


class Travel(BasePydanticModel):
    id: int | None
    owner_id: int
    title: str
    description: str
    locates: list["Location"]
