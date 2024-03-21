from datetime import datetime

from core.models import City, Country
from core.models.base import BasePydanticModel
from core.models.travel import Travel

MAX_LOCATION_TITLE_LENGTH = 1024
MAX_LOCATION_ADDRESS_LENGTH = 512


class Location(BasePydanticModel):
    id: int | None = None
    travel_id: int
    title: str
    country_id: int
    city_id: int
    address: str
    start_at: datetime
    end_at: datetime


class LocationExtended(Location):
    id: int
    travel: Travel
    country: Country
    city: City
