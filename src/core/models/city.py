from pydantic import Field

from core.models.base import BaseCoreModel
from core.models.country import Country

MAX_CITY_LENGTH = 256
MAX_TIMEZONE_LENGTH = 128


class City(BaseCoreModel):
    id: int | None = None
    country_id: int
    title: str = Field(min_length=1, max_length=MAX_CITY_LENGTH)
    latitude: float
    longitude: float
    timezone: str = Field(min_length=1, max_length=MAX_TIMEZONE_LENGTH)


class CityExtended(City):
    id: int
    country: Country
