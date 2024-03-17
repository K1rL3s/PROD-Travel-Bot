from abc import ABC

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery

from bot.callbacks.state import InStateData
from bot.utils.enums import Action


class BaseScene(Scene, ABC):
    @on.callback_query(InStateData.filter(F.action == Action.BACK))
    async def back(self, callback: CallbackQuery, state: FSMContext) -> None:
        data = await state.get_data()
        step = data["step"]

        previous_step = step - 1
        if previous_step < 0:
            return await self.exit(callback)
        return await self.wizard.back(step=previous_step)

    @on.callback_query(InStateData.filter(F.action == Action.CANCEL))
    async def exit(self, callback: CallbackQuery) -> None:
        await callback.message.edit_text("Окей, отмена")
        await self.wizard.exit()

    @on.callback_query.exit()
    async def on_callback_exit(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        await state.set_data({})
