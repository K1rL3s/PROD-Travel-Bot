from datetime import datetime
from typing import TYPE_CHECKING

from core.models.base import BasePydanticModel

if TYPE_CHECKING:
    from core.models.travel import Travel


class Location(BasePydanticModel):
    id: int | None
    travel_id: int
    order: int
    title: str
    country: str
    city: str
    address: str
    start_at: datetime
    end_at: datetime

    travels: list["Travel"]
