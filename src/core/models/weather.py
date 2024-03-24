from core.models.base import BaseCoreModel


class Weather(BaseCoreModel):
    temp: float
    temp_min: float
    temp_max: float
    feels_like: float
    pressure: int
    humidity: int
    visibility: int
    wind_speed: float
    description: str
