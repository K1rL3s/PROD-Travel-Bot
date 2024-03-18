from pydantic import Field

from core.models.base import BasePydanticModel

MAX_USER_NAME_LENGTH = 128
MAX_USER_COUNTRY_LENGTH = 128
MAX_USER_CITY_LENGTH = 128
MAX_USER_DESCRIPTION_LENGTH = 256


class User(BasePydanticModel):
    id: int
    name: str = Field(min_length=1, max_length=MAX_USER_NAME_LENGTH)
    age: int
    country: str = Field(min_length=1, max_length=MAX_USER_COUNTRY_LENGTH)
    city: str = Field(min_length=1, max_length=MAX_USER_CITY_LENGTH)
    description: str | None = Field(max_length=MAX_USER_DESCRIPTION_LENGTH)
