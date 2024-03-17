from dataclasses import dataclass
from typing import Any

from aiogram import Bot, F, html
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import on
from aiogram.types import CallbackQuery, Message

from bot.handlers.base_scene import BaseScene
from bot.handlers.profile.phrases import error_text_by_field
from bot.keyboards.profile import check_profile_keyboard
from bot.keyboards.universal import back_cancel_keyboard
from bot.utils.enums import ProfileFields
from bot.utils.tg import delete_last_message
from core.models import User
from core.service.user import UserService, get_user_field_validator


@dataclass
class Question:
    text: str
    key: str


profile_fill_steps = [
    Question(text="Как вас зовут?", key="name"),
    Question(text="Сколько вам лет?", key="age"),
    Question(text="В каком городе вы живёте?", key="city"),
    Question(
        text="Расскажите о себе. Это будет описанием вашего профиля.",
        key="description",
    ),
]


class ProfileFillScene(BaseScene, state="profile"):
    @on.callback_query.enter()
    async def on_callback_enter(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        step: int = 0,
    ) -> None:
        try:
            question = profile_fill_steps[step]
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
            question = profile_fill_steps[step]
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
    ) -> None:
        data = await state.get_data()
        step: int = data["step"]
        answers: dict[str, Any] = data.get("answers", {})
        question = profile_fill_steps[step]

        if error := self.step_answer_check(message.text, question.key):
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
        if len(answers) != len(profile_fill_steps):
            await message.answer(text="Жаль...")
            return

        user = User(
            id=message.from_user.id,
            name=html.quote(answers["name"]),
            age=int(answers["age"]),
            city=html.quote(answers["city"]),
            description=html.quote(answers["description"]),
            country="timecountry",
        )
        await user_service.create(user)
        await message.answer(
            text="Профиль успешно создан!",
            reply_markup=check_profile_keyboard,
        )

        await delete_last_message(bot, state, message)
        await state.set_data({})

    def step_answer_check(
        self,
        answer: str,
        field: str,
    ) -> str | None:
        validators = {
            field: (get_user_field_validator(field), error_text_by_field[field])
            for field in ProfileFields.values()
        }
        validator, error_text = validators.get(field)
        if not validator(answer):
            return error_text
