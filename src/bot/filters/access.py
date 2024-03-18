from abc import ABC
from typing import Any, Callable, Generic, Protocol, TypeVar

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.models import User

M = TypeVar("M")
K = TypeVar("K")


class Service(Protocol[M, K]):
    async def get_with_access_check(self, tg_id: int, obj_id: K) -> M:
        pass

    async def is_owner(self, tg_id: int, obj_id: K) -> bool:
        pass


class BaseAccessFilter(BaseFilter, Generic[M, K], ABC):
    def __init__(
        self,
        service_context_var: str,
        add_context_var: str,
        owner_mode: bool = False,
    ) -> None:
        self.service_context_var = service_context_var
        self.add_context_var = add_context_var
        self.owner_mode = owner_mode

    async def owner_access(
        self,
        tg_id: int,
        obj_id: K,
        service: Service[M, K],
    ) -> bool | dict[str, Any]:
        if not await service.is_owner(tg_id, obj_id):
            return False

        obj = await service.get_with_access_check(tg_id, obj_id)
        if obj:
            return {self.add_context_var: obj}
        return False

    async def default_access(
        self,
        tg_id: int,
        obj_id: K,
        service: Service[M, K],
    ) -> bool | dict[str, Any]:
        obj = await service.get_with_access_check(tg_id, obj_id)
        if obj:
            return {self.add_context_var: obj}
        return False


class CallbackAccess(BaseAccessFilter[M, K], ABC):
    def __init__(
        self,
        service_context_var: str,
        add_context_var: str,
        callback_data_checker: Callable[[Any], K],
        owner_mode: bool = False,
    ) -> None:
        super().__init__(
            service_context_var=service_context_var,
            add_context_var=add_context_var,
            owner_mode=owner_mode,
        )
        self.callback_data_checker = callback_data_checker

    async def __call__(
        self,
        callback: CallbackQuery,
        callback_data: Any,
        **kwargs: Any,
    ) -> bool | dict[str, Any]:
        obj_id = self.callback_data_checker(callback_data)
        if obj_id is None:
            return False

        tg_id = callback.from_user.id
        service: Service[M, K] = kwargs[self.service_context_var]

        if self.owner_mode:
            return await self.owner_access(tg_id, obj_id, service)
        return await self.default_access(tg_id, obj_id, service)


class StateAccess(BaseAccessFilter[M, K], ABC):
    def __init__(
        self,
        service_context_var: str,
        add_context_var: str,
        state_key: str,
        owner_mode: bool = False,
    ) -> None:
        super().__init__(
            service_context_var=service_context_var,
            add_context_var=add_context_var,
            owner_mode=owner_mode,
        )
        self.state_key = state_key

    async def __call__(
        self,
        event: Any,
        state: FSMContext,
        user: User,
        **kwargs: Any,
    ) -> bool | dict[str, Any]:
        data = await state.get_data()
        obj_id: K | None = data.get(self.state_key)

        if obj_id is None:
            return False

        tg_id = user.id
        service: Service[M, K] = kwargs[self.service_context_var]

        if self.owner_mode:
            return await self.owner_access(tg_id, obj_id, service)
        return await self.default_access(tg_id, obj_id, service)
