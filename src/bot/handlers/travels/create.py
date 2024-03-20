from dataclasses import dataclass
from typing import Any, Awaitable, Callable, TypeVar

from aiogram import Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import on
from aiogram.types import CallbackQuery, Message

from bot.callbacks import InStateData
from bot.handlers.base_scene import BaseScene
from bot.keyboards import back_cancel_keyboard, one_travel_keyboard, travels_keyboard
from bot.utils.enums import Action
from bot.utils.html import html_quote
from bot.utils.tg import delete_last_message
from core.models import Travel
from core.services import TravelService, get_travel_field_validator
from core.utils.enums import TravelField

from .funcs import format_travel
from .phrases import error_text_by_field

T = TypeVar("T")


@dataclass
class Question:
    text: str
    key: str


travel_create_steps = [
    Question(text="Как будет называться это путешествие?", key="title"),
    Question(
        text="Кратко опишите его. Что посетите, чего ожидаете?",
        key="description",
    ),
]


class TravelCreateScene(BaseScene, state="travel"):
    @on.callback_query.enter()
    async def on_callback_enter(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        step: int = 0,
    ) -> None:
        try:
            question = travel_create_steps[step]
        except IndexError:
            return await self.wizard.exit()

        await state.update_data(step=step, last_id=callback.message.message_id)
        await callback.message.edit_text(
            text=question.text,
            reply_markup=back_cancel_keyboard,
        )

    @on.message.enter()
    async def on_message_enter(
        self,
        message: Message,
        bot: Bot,
        state: FSMContext,
        step: int = 0,
    ) -> None:
        try:
            question = travel_create_steps[step]
        except IndexError:
            return await self.wizard.exit()

        bot_message = await message.answer(
            text=question.text,
            reply_markup=back_cancel_keyboard,
        )
        await delete_last_message(bot, state, message)
        await state.update_data(step=step, last_id=bot_message.message_id)

    @on.message(F.text)
    async def answer(
        self,
        message: Message,
        bot: Bot,
        state: FSMContext,
        travel_service: TravelService,
    ) -> None:
        data = await state.get_data()
        step: int = data["step"]
        answers: dict[str, Any] = data.get("answers", {})
        question = travel_create_steps[step]

        value, error = await self.step_answer_check(
            message.text,
            question.key,
            travel_service,
        )
        if error:
            await message.reply(text=error, reply_markup=back_cancel_keyboard)
            await delete_last_message(bot, state, message)
            return

        answers[question.key] = message.text

        await state.update_data(answers=answers)
        await self.wizard.retake(step=step + 1)

    @on.message.exit()
    async def on_message_exit(
        self,
        message: Message,
        bot: Bot,
        state: FSMContext,
        travel_service: TravelService,
    ) -> None:
        data = await state.get_data()
        answers = data["answers"]

        travel = Travel(
            owner_id=message.from_user.id,
            title=html_quote(answers["title"]),
            description=html_quote(answers["description"]),
        )
        travel = await travel_service.create(travel)
        await message.answer(
            text=format_travel(travel),
            reply_markup=one_travel_keyboard(travel, message.from_user.id, page=0),
        )

        await delete_last_message(bot, state, message)
        await state.set_data({})

    @on.callback_query(InStateData.filter(F.action == Action.CANCEL))
    async def exit_callback(self, callback: CallbackQuery) -> None:
        await self.wizard.exit()

    @on.callback_query.exit()
    async def on_callback_exit(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        travel_service: TravelService,
    ) -> None:
        text = "Ваши путешествия"
        keyboard = await travels_keyboard(callback.from_user.id, 0, travel_service)
        await callback.message.edit_text(text=text, reply_markup=keyboard)
        await state.set_data({})

    async def step_answer_check(
        self,
        answer: str,
        field: str,
        travel_service: TravelService,
    ) -> tuple[str | None, str | None]:
        validators: dict[
            str, tuple[Callable[[TravelService, T], Awaitable[T | None]], str]
        ] = {
            field: (get_travel_field_validator(field), error_text_by_field[field])
            for field in TravelField.values()
        }
        validator, error_text = validators[field]
        if (value := await validator(travel_service, answer)) is None:
            return None, error_text
        return value, None
