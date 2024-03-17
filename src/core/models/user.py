from core.models.base import BasePydanticModel


class User(BasePydanticModel):
    id: int
    name: str
    age: int
    city: str
    country: str
    description: str
