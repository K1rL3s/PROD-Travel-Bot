import contextlib
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Awaitable, Callable, TypeVar

from aiogram import Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import on
from aiogram.types import CallbackQuery, Message

from bot.callbacks.locations import AddLocationData
from bot.callbacks.state import InStateData
from bot.handlers.base_scene import BaseScene
from bot.keyboards.locations import locations_keyboard, one_location_keyboard
from bot.keyboards.universal import back_cancel_keyboard
from bot.utils.enums import Action
from bot.utils.html import html_quote
from bot.utils.tg import delete_last_message
from core.models import Location
from core.service.location import LocationService, get_location_field_validator
from core.service.travel import TravelService
from core.utils.enums import LocationField

from .funcs import format_location
from .phrases import error_text_by_field

T = TypeVar("T")


@dataclass
class Question:
    text: str
    key: str


location_create_steps = [
    Question(text="Как называется это место?", key="title"),
    Question(text="В каком городе это место?", key="city"),
    Question(text="В какой стране это место?", key="country"),
    Question(text="Какой адрес этого места?", key="address"),
    Question(text="Когда вы хотите посетить это место?", key="start_at"),
    Question(text="До скольки вы будете в этом месте?", key="end_at"),
]


class LocationCreateScene(BaseScene, state="location"):
    @on.callback_query.enter()
    async def on_callback_enter(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        step: int = 0,
    ) -> None:
        try:
            question = location_create_steps[step]
        except IndexError:
            return await self.wizard.exit()

        new_data = {"step": step, "last_id": callback.message.message_id}
        with contextlib.suppress(TypeError, ValueError):
            callback_data = AddLocationData.unpack(callback.data)
            new_data.update(
                {"travel_id": callback_data.travel_id, "page": callback_data.page}
            )
        await state.update_data(**new_data)

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
            question = location_create_steps[step]
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
        location_service: LocationService,
    ) -> None:
        data = await state.get_data()
        step: int = data["step"]
        answers: dict[str, Any] = data.get("answers", {})
        question = location_create_steps[step]

        value, error = await self.step_answer_check(
            message.text,
            question.key,
            location_service,
        )
        if error:
            await message.reply(text=error, reply_markup=back_cancel_keyboard)
            await delete_last_message(bot, state, message)
            return

        answers[question.key] = value

        await state.update_data(answers=answers)
        await self.wizard.retake(step=step + 1)

    @on.message.exit()
    async def on_message_exit(
        self,
        message: Message,
        bot: Bot,
        state: FSMContext,
        location_service: LocationService,
    ) -> None:
        data = await state.get_data()
        answers: dict[str, Any] = data["answers"]

        location = Location(
            travel_id=data["travel_id"],
            title=html_quote(answers["title"]),
            country=html_quote(answers["country"]),
            city=html_quote(answers["city"]),
            address=html_quote(answers["address"]),
            start_at=datetime.utcnow(),  # !!
            end_at=datetime.utcnow(),  # !!
        )
        location_ext = await location_service.create(location)
        await message.answer(
            text=format_location(location_ext),
            reply_markup=one_location_keyboard(
                location_ext,
                message.from_user.id,
                page=0,
            ),
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
        location_service: LocationService,
        travel_service: TravelService,
    ) -> None:
        data = await state.get_data()
        travel_id: int = data["travel_id"]

        text = "Локации путешествия"
        keyboard = await locations_keyboard(
            callback.from_user.id,
            0,
            travel_id,
            location_service,
            travel_service,
        )
        await callback.message.edit_text(text=text, reply_markup=keyboard)
        await state.set_data({})

    async def step_answer_check(
        self,
        answer: str,
        field: str,
        location_service: LocationService,
    ) -> tuple[str | None, str | None]:
        validators: dict[
            str, tuple[Callable[[LocationService, T], Awaitable[T | None]], str]
        ] = {
            field: (get_location_field_validator(field), error_text_by_field[field])
            for field in LocationField.values()
        }
        validator, error_text = validators[field]
        if (value := await validator(location_service, answer)) is None:
            return None, error_text
        return value, None
