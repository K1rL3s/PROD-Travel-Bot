from abc import ABC, abstractmethod


class Timezoner(ABC):
    @abstractmethod
    async def get_timezone(self, latitude: float, longitude: float) -> str:
        pass
