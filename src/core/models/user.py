from pydantic import Field

from core.models import City, Country
from core.models.base import BasePydanticModel

MAX_USER_NAME_LENGTH = 128
MAX_USER_DESCRIPTION_LENGTH = 256


class User(BasePydanticModel):
    id: int
    name: str = Field(min_length=1, max_length=MAX_USER_NAME_LENGTH)
    age: int
    city_id: int
    country_id: int
    description: str | None = Field(None, max_length=MAX_USER_DESCRIPTION_LENGTH)


class UserExtended(User):
    city: City
    country: Country
