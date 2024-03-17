import contextlib

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


async def delete_last_message(
    bot: Bot,
    state: FSMContext,
    message: Message,
) -> None:
    data = await state.get_data()
    last_id: int | None = data.get("last_id")

    if last_id is not None:
        with contextlib.suppress(TelegramAPIError):
            await bot.delete_message(chat_id=message.chat.id, message_id=last_id)
