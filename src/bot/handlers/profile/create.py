from dataclasses import dataclass
from typing import Any

from aiogram import Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import on
from aiogram.types import CallbackQuery, Message

from bot.callbacks.state import InStateData
from bot.handlers.base_scene import BaseScene
from bot.keyboards.start import start_keyboard
from bot.keyboards.universal import back_cancel_keyboard
from bot.utils.enums import Action
from bot.utils.html import html_quote
from bot.utils.tg import delete_last_message
from core.models import User
from core.service.user import UserService, get_user_field_validator
from core.utils.enums import ProfileField

from .phrases import error_text_by_field


@dataclass
class Question:
    text: str
    key: str


profile_create_steps = [
    Question(text="Как вас зовут?", key="name"),
    Question(text="Сколько вам лет?", key="age"),
    Question(text="В каком городе вы живёте?", key="city"),
    Question(
        text="Расскажите о себе. Это будет описанием вашего профиля.",
        key="description",
    ),
]


class ProfileCreateScene(BaseScene, state="profile"):
    @on.callback_query.enter()
    async def on_callback_enter(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        step: int = 0,
    ) -> None:
        try:
            question = profile_create_steps[step]
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
            question = profile_create_steps[step]
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
        user_service: UserService,
    ) -> None:
        data = await state.get_data()
        step: int = data["step"]
        answers: dict[str, Any] = data.get("answers", {})
        question = profile_create_steps[step]

        if error := await self.step_answer_check(
            message.text,
            question.key,
            user_service,
        ):
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
        user_service: UserService,
    ) -> None:
        data = await state.get_data()
        answers = data.get("answers", {})
        if len(answers) != len(profile_create_steps):
            await message.answer(text="Жаль...")
            return

        user = User(
            id=message.from_user.id,
            name=html_quote(answers["name"]),
            age=int(answers["age"]),
            city=html_quote(answers["city"]),
            description=html_quote(answers["description"]),
            country="timecountry",
        )
        await user_service.create(user)
        await message.answer(
            text="Профиль успешно создан!",
            reply_markup=start_keyboard,
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
    ) -> None:
        await callback.message.edit_text("Окей, отмена.")
        await state.set_data({})

    async def step_answer_check(
        self,
        answer: str,
        field: str,
        user_service: UserService,
    ) -> str | None:
        validators = {
            field: (get_user_field_validator(field), error_text_by_field[field])
            for field in ProfileField.values()
        }
        validator, error_text = validators[field]
        if not await validator(user_service, answer):
            return error_text
