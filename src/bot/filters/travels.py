from abc import ABC
from typing import Any

from bot.filters.access import CallbackAccess, StateAccess
from core.models import TravelExtended


class TravelCallbackBase(CallbackAccess[TravelExtended, int], ABC):
    @staticmethod
    def _check_callback_data(callback_data: Any) -> int | None:
        if hasattr(callback_data, "travel_id") and isinstance(
            callback_data.travel_id, int
        ):
            return callback_data.travel_id
        return None


class TravelCallbackAccess(TravelCallbackBase):
    def __init__(self) -> None:
        super().__init__(
            service_context_var="travel_service",
            add_context_var="travel",
            owner_mode=False,
        )


class TravelCallbackOwner(TravelCallbackBase):
    def __init__(self) -> None:
        super().__init__(
            service_context_var="travel_service",
            add_context_var="travel",
            owner_mode=True,
        )


class TravelStateAccess(StateAccess[TravelExtended, int]):
    def __init__(self) -> None:
        super().__init__(
            service_context_var="travel_service",
            add_context_var="travel",
            state_key="travel_id",
            owner_mode=False,
        )


class TravelStateOwner(StateAccess[TravelExtended, int]):
    def __init__(self) -> None:
        super().__init__(
            service_context_var="travel_service",
            add_context_var="travel",
            state_key="travel_id",
            owner_mode=True,
        )
