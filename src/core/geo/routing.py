from abc import ABC, abstractmethod


class Routing(ABC):
    @abstractmethod
    def route_url(self, points: list[tuple[float, float]]) -> str:
        pass

    @abstractmethod
    async def route_image(
        self, points_lon_lat: list[tuple[float, float]]
    ) -> bytes | None:
        pass
