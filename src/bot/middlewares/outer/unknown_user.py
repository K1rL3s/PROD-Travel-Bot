from collections.abc import Awaitable, Callable
from typing import Any, cast

from aiogram import Bot
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Chat, Message, Update

from bot.callbacks import ProfileData
from bot.keyboards import fill_profile_keyboard
from bot.middlewares.base import BaseInfoMiddleware
from bot.utils.enums import SlashCommand
from bot.utils.states import ProfileCreating
from core.models import User


class UnknownUserMiddleware(BaseInfoMiddleware):
    """Мидлварь, который не даёт доступ к боту незарегистрированным пользователям."""

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        bot: Bot = data["bot"]
        user: User | None = data.get("user")
        raw_state: str | None = data.get("raw_state")

        if user is not None:
            return await handler(event, data)
        if ProfileCreating()(event, raw_state):
            return await handler(event, data)

        if isinstance(event.event, Message):
            message = cast(Message, event.event)
            if await Command(SlashCommand.START)(message, bot):
                return await handler(event, data)
            if await Command(SlashCommand.HELP)(message, bot):
                return await handler(event, data)

        if isinstance(event.event, CallbackQuery):
            callback = cast(CallbackQuery, event.event)
            if await ProfileData.filter()(callback):
                return await handler(event, data)

        event_chat: Chat | None = data.get("event_chat")
        if not event_chat:
            return None

        await bot.send_message(
            chat_id=event_chat.id,
            text="Я тебя не знаю, зарегистрируйся!",
            reply_markup=fill_profile_keyboard,
        )
