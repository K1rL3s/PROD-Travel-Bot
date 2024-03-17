from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.utils.enums import SlashCommand, TextCommand

router = Router(name=__name__)


@router.message(F.text == TextCommand.CANCEL, StateFilter("*"))
@router.message(
    Command(SlashCommand.CANCEL, SlashCommand.STOP),
    StateFilter("*"),
)
async def cancel_message_text(
    message: "Message",
    state: "FSMContext",
) -> None:
    """Обработчик команд "/cancel", "/stop"."""
    if await state.get_state() is None:
        return

    await state.clear()
