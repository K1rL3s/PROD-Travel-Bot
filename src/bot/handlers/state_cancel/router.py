from aiogram import F, Router
from aiogram.filters import Command, MagicData, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards import fill_profile_keyboard, start_keyboard
from bot.utils.enums import SlashCommand, TextCommand

cancel_state_router = Router(name=__name__)


@cancel_state_router.message(
    F.text == TextCommand.CANCEL,
    StateFilter("*"),
    ~MagicData(F.user),
)
@cancel_state_router.message(
    Command(SlashCommand.CANCEL, SlashCommand.STOP),
    StateFilter("*"),
    ~MagicData(F.user),
)
async def cancel_message_unknonw(
    message: "Message",
    state: "FSMContext",
) -> None:
    """Обработчик команд "/cancel", "/stop"."""
    text = "Ок!"
    keyboard = fill_profile_keyboard
    await message.answer(text=text, reply_markup=keyboard)
    await state.clear()


@cancel_state_router.message(
    F.text == TextCommand.CANCEL,
    StateFilter("*"),
    MagicData(F.user),
)
@cancel_state_router.message(
    Command(SlashCommand.CANCEL, SlashCommand.STOP),
    StateFilter("*"),
    MagicData(F.user),
)
async def cancel_message_knonw(
    message: "Message",
    state: "FSMContext",
) -> None:
    """Обработчик команд "/cancel", "/stop"."""
    text = "Ок!"
    keyboard = start_keyboard
    await message.answer(text=text, reply_markup=keyboard)
    await state.clear()
