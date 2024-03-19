from typing import Any

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.repositories import UserRepo
from core.service.user import UserService


def _check_callback_data(callback_data: Any) -> int | None:
    if hasattr(callback_data, "member_id") and isinstance(callback_data.member_id, int):
        return callback_data.member_id
    return None


class MemberCallbackDI(BaseFilter):
    async def __call__(
        self,
        callback: CallbackQuery,
        callback_data: Any,
        **kwargs: Any,
    ) -> bool | dict[str, Any]:
        member_id = _check_callback_data(callback_data)
        if member_id is None:
            return False

        service: UserService = kwargs["user_service"]

        member = await service.get(member_id)
        if member:
            return {"member": member}
        return False


class MemberStateDI(BaseFilter):
    async def __call__(
        self,
        event: Any,
        state: FSMContext,
        **kwargs: Any,
    ) -> bool | dict[str, Any]:
        data = await state.get_data()
        member_id: int | None = data.get("member_id")

        if member_id is None:
            return False

        repo: UserRepo = kwargs["user_repo"]

        member = await repo.get(member_id)
        if member:
            return {"member": member}
        return False
