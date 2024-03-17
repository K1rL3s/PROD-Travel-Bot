from typing import Any

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, User

from core.service.travel import TravelService


class TravelCallbackAccess(BaseFilter):
    async def __call__(
        self,
        callback: CallbackQuery,
        callback_data: Any,
        travel_service: TravelService,
    ) -> bool | dict[str, Any]:
        if not hasattr(callback_data, "id"):
            return False
        if not isinstance(callback_data.id, int):
            return False

        travel = await travel_service.get_with_access_check(
            callback.from_user.id,
            callback_data.id,
        )
        if travel is None:
            return False
        return {"travel": travel}


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
