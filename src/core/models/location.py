from datetime import datetime

from core.models.base import BasePydanticModel


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
