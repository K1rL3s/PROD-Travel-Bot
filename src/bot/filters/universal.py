from typing import Any

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext


class FieldInState(BaseFilter):
    def __init__(self, field_value: Any, field_key: str = "field") -> None:
        self.field_value = field_value
        self.field_key = field_key

    async def __call__(self, event: Any, state: FSMContext) -> bool:
        data = await state.get_data()
        return data.get(self.field_key) == self.field_value
