from aiogram import F, Router
from aiogram.filters import Command, CommandStart, MagicData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.menu import OpenMenu
from bot.keyboards.profile import check_profile_keyboard, fill_profile_keyboard
from bot.utils.enums import BotMenu

router = Router(name=__name__)


@router.message(CommandStart(), MagicData(F.user))
async def start_command_known(message: Message, state: FSMContext) -> None:
    text = "Привет! Я тебя знаю"
    keyboard = check_profile_keyboard
    await message.answer(text=text, reply_markup=keyboard)
    await state.clear()


@router.message(CommandStart())
async def start_command_unknown(message: Message) -> None:
    text = "Привет! Ты новенький, зарегистрируйся"
    keyboard = fill_profile_keyboard
    await message.answer(text=text, reply_markup=keyboard)


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(text="Помощь!")


@router.callback_query(OpenMenu.filter(F.menu == BotMenu.START))
async def start_callback(callback: CallbackQuery, state: FSMContext) -> None:
    text = "Привет! Я тебя знаю"
    keyboard = check_profile_keyboard
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await state.clear()
