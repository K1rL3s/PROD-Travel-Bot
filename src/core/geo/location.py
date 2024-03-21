from abc import ABC, abstractmethod
from typing import Any

from core.geo.point import GeoPoint


class GeoLocation(ABC):
    @property
    @abstractmethod
    def local_title(self) -> str | None:
        pass

    @property
    @abstractmethod
    def country_title(self) -> str | None:
        pass

    @property
    @abstractmethod
    def country_code(self) -> str | None:
        pass

    @property
    @abstractmethod
    def address(self) -> str:
        pass

    @property
    @abstractmethod
    def latitude(self) -> float:
        pass

    @property
    @abstractmethod
    def longitude(self) -> float:
        pass

    @property
    @abstractmethod
    def altitude(self) -> float:
        pass

    @property
    @abstractmethod
    def point(self) -> GeoPoint:
        pass

    @property
    @abstractmethod
    def raw(self) -> dict:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __getstate__(self) -> tuple[Any, GeoPoint, Any]:
        pass

    @abstractmethod
    def __setstate__(self, state):
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @abstractmethod
    def __ne__(self, other) -> bool:
        return not (self == other)

    @abstractmethod
    def __len__(self) -> int:
        return len(self._tuple)  # type: ignore
