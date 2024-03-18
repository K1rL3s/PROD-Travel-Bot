from typing import Any

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, User

from core.service.travel import TravelService


def _check_callback_data(callback_data: Any) -> bool:
    return hasattr(callback_data, "travel_id") and isinstance(
        callback_data.travel_id, int
    )


class TravelCallbackAccess(BaseFilter):
    async def __call__(
        self,
        callback: CallbackQuery,
        callback_data: Any,
        travel_service: TravelService,
    ) -> bool | dict[str, Any]:
        if not _check_callback_data(callback_data):
            return False

        travel = await travel_service.get_with_access_check(
            callback.from_user.id,
            callback_data.travel_id,
        )
        if travel:
            return {"travel": travel}
        return False


class TravelCallbackOwner(BaseFilter):
    async def __call__(
        self,
        callback: CallbackQuery,
        callback_data: Any,
        travel_service: TravelService,
    ) -> bool | dict[str, Any]:
        if not _check_callback_data(callback_data):
            return False

        if not await travel_service.is_owner(
            callback.from_user.id,
            callback_data.travel_id,
        ):
            return False

        travel = await travel_service.get_with_access_check(
            callback.from_user.id,
            callback_data.travel_id,
        )
        if travel:
            return {"travel": travel}
        return False


class TravelStateAccess(BaseFilter):
    async def __call__(
        self,
        event: Any,
        state: FSMContext,
        user: User,
        travel_service: TravelService,
    ) -> bool | dict[str, Any]:
        data = await state.get_data()
        travel_id: int | None = data.get("travel_id")

        if travel_id is None:
            return False

        travel = await travel_service.get_with_access_check(user.id, travel_id)
        if travel is None:
            return False

        return {"travel": travel}


class TravelStateOwner(BaseFilter):
    async def __call__(
        self,
        event: Any,
        state: FSMContext,
        user: User,
        travel_service: TravelService,
    ) -> bool | dict[str, Any]:
        data = await state.get_data()
        travel_id: int | None = data.get("travel_id")

        if travel_id is None:
            return False
        if not await travel_service.is_owner(user.id, travel_id):
            return False

        travel = await travel_service.get_with_access_check(user.id, travel_id)
        if travel:
            return {"travel": travel}
        return False
