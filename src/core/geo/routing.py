from abc import ABC, abstractmethod


class Routing(ABC):
    @abstractmethod
    def route_url(self, points: list[tuple[float, float]]) -> str:
        pass
