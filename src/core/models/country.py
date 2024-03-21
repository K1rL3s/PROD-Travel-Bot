from pydantic import Field

from core.models.base import BasePydanticModel

MAX_COUNTRY_LENGTH = 256


class Country(BasePydanticModel):
    id: int | None = None
    title: str = Field(min_length=1, max_length=MAX_COUNTRY_LENGTH)
    alpha2: str


class CountryExtended(Country):
    id: int
