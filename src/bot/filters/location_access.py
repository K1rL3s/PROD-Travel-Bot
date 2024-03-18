from typing import Any

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, User

from core.service.location import LocationService


def _check_callback_data(callback_data: Any) -> bool:
    return hasattr(callback_data, "location_id") and isinstance(
        callback_data.location_id, int
    )


class LocationCallbackAccess(BaseFilter):
    async def __call__(
        self,
        callback: CallbackQuery,
        callback_data: Any,
        location_service: LocationService,
    ) -> bool | dict[str, Any]:
        if not _check_callback_data(callback_data):
            return False

        location = await location_service.get_with_access_check(
            callback.from_user.id,
            callback_data.location_id,
        )

        if location:
            return {"location": location}
        return False


class LocationCallbackOwner(BaseFilter):
    async def __call__(
        self,
        callback: CallbackQuery,
        callback_data: Any,
        location_service: LocationService,
    ) -> bool | dict[str, Any]:
        if not _check_callback_data(callback_data):
            return False

        if not await location_service.is_owner(
            callback.from_user.id,
            callback_data.location_id,
        ):
            return False

        location = await location_service.get_with_access_check(
            callback.from_user.id,
            callback_data.location_id,
        )
        if location:
            return {"location": location}
        return False


class LocationStateAccess(BaseFilter):
    async def __call__(
        self,
        event: Any,
        state: FSMContext,
        user: User,
        location_service: LocationService,
    ) -> bool | dict[str, Any]:
        data = await state.get_data()
        location_id: int | None = data.get("location_id")

        if location_id is None:
            return False

        location = await location_service.get_with_access_check(user.id, location_id)
        if location is None:
            return False

        return {"location": location}


class LocationStateOwner(BaseFilter):
    async def __call__(
        self,
        event: Any,
        state: FSMContext,
        user: User,
        location_service: LocationService,
    ) -> bool | dict[str, Any]:
        data = await state.get_data()
        location_id: int | None = data.get("location_id")

        if location_id is None:
            return False
        if not await location_service.is_owner(user.id, location_id):
            return False

        location = await location_service.get_with_access_check(user.id, location_id)
        if location:
            return {"location": location}
        return False
