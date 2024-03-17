from collections.abc import Awaitable, Callable
from typing import Any, cast

from aiogram import Bot
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Chat, Message, Update

from bot.callbacks.profile import ProfileData
from bot.keyboards.profile import fill_profile_keyboard
from bot.middlewares.base import BaseInfoMiddleware
from bot.utils.enums import TextCommand
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

        if user is not None:
            return await handler(event, data)

        if isinstance(event.event, Message):
            message = cast(Message, event.event)
            if await Command(TextCommand.START)(message, bot):
                return await handler(event, data)
            if await Command(TextCommand.HELP)(message, bot):
                return await handler(event, data)

        if isinstance(event.event, CallbackQuery):
            callback = cast(CallbackQuery, event.event)
            if await ProfileData.filter()(callback):
                return await handler(event, data)

        event_chat: Chat | None = data.get("event_chat")
        if not event_chat:
            return

        await bot.send_message(
            chat_id=event_chat.id,
            text="Я тебя не знаю, зарегистрируйся!",
            reply_markup=fill_profile_keyboard,
        )
