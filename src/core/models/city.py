from pydantic import Field

from core.models.base import BasePydanticModel
from core.models.country import Country

MAX_CITY_LENGTH = 256


class City(BasePydanticModel):
    id: int | None = None
    title: str = Field(min_length=1, max_length=MAX_CITY_LENGTH)
    country_id: int
    latitude: float
    longitude: float


class CityExtended(City):
    id: int
    country: Country
