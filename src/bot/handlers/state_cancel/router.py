from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.utils.enums import SlashCommand, TextCommand

cancel_state_router = Router(name=__name__)


@cancel_state_router.message(F.text == TextCommand.CANCEL, StateFilter("*"))
@cancel_state_router.message(
    Command(SlashCommand.CANCEL, SlashCommand.STOP),
    StateFilter("*"),
)
async def cancel_message_text(
    message: "Message",
    state: "FSMContext",
) -> None:
    """Обработчик команд "/cancel", "/stop"."""
    await message.answer("Ок!")

    if await state.get_state() is None:
        return

    await state.clear()
