from abc import ABC
from typing import Any

from bot.filters.access import CallbackAccess, StateAccess
from core.models import LocationExtended


class LocationCallbackBase(CallbackAccess[LocationExtended, int], ABC):
    @staticmethod
    def _check_callback_data(callback_data: Any) -> int | None:
        if hasattr(callback_data, "location_id") and isinstance(
            callback_data.location_id, int
        ):
            return callback_data.location_id
        return None


class LocationCallbackAccess(LocationCallbackBase):
    def __init__(self) -> None:
        super().__init__(
            service_context_var="location_service",
            add_context_var="location",
            owner_mode=False,
        )


class LocationCallbackOwner(LocationCallbackBase):
    def __init__(self) -> None:
        super().__init__(
            service_context_var="location_service",
            add_context_var="location",
            owner_mode=True,
        )


class LocationStateAccess(StateAccess[LocationExtended, int]):
    def __init__(self) -> None:
        super().__init__(
            service_context_var="location_service",
            add_context_var="location",
            state_key="location_id",
            owner_mode=False,
        )


class LocationStateOwner(StateAccess[LocationExtended, int]):
    def __init__(self) -> None:
        super().__init__(
            service_context_var="location_service",
            add_context_var="location",
            state_key="location_id",
            owner_mode=True,
        )
