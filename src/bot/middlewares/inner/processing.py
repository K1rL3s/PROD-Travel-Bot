from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import html
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message

from bot.middlewares.base import BaseInfoMiddleware

PROCESSING = f"{html.italic('⚙️⏳ Уточняю данные, секунду...')}"


class ProcessingMiddleware(BaseInfoMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        processing = get_flag(data, "processing")
        if not processing:
            return await handler(event, data)

        bot_msg = await event.answer(text=PROCESSING)
        try:
            return await handler(event, data)
        finally:
            await bot_msg.delete()
