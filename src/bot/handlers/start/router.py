from aiogram import F, Router
from aiogram.filters import Command, CommandStart, MagicData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.menu import OpenMenu
from bot.keyboards.start import fill_profile_keyboard, start_keyboard
from bot.utils.enums import BotMenu

start_router = Router(name=__name__)


@start_router.message(CommandStart(), MagicData(F.user))
async def start_command_known(message: Message, state: FSMContext) -> None:
    text = "Привет! Я тебя знаю"
    await message.answer(text=text, reply_markup=start_keyboard)
    await state.clear()


@start_router.message(CommandStart())
async def start_command_unknown(message: Message) -> None:
    text = "Привет! Ты новенький, зарегистрируйся"
    await message.answer(text=text, reply_markup=fill_profile_keyboard)


@start_router.message(Command("help"), MagicData(F.user))
async def help_command_known(message: Message) -> None:
    await message.answer(text="Помощь!", reply_markup=start_keyboard)


@start_router.message(Command("help"))
async def help_command_unknown(message: Message) -> None:
    await message.answer(text="Помощь!", reply_markup=fill_profile_keyboard)


@start_router.callback_query(OpenMenu.filter(F.menu == BotMenu.START))
async def start_callback(callback: CallbackQuery, state: FSMContext) -> None:
    text = "Привет! Я тебя знаю"
    await callback.message.edit_text(text=text, reply_markup=start_keyboard)
    await state.clear()
