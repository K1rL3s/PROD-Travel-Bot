from uuid import UUID

from aiogram import F, Router
from aiogram.filters import Command, CommandStart, MagicData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks import OpenMenu
from bot.keyboards import check_joined_travel, fill_profile_keyboard, start_keyboard
from bot.utils.enums import BotMenu
from core.models.invite_link import INVITE_LINK_ID_REGEX
from core.services import MemberService

from .phrases import (
    BAD_INVITE_LINK,
    HELP_TEXT,
    NEW_USER_TEXT,
    START_TEXT,
    TRAVEL_JOINED,
)

start_router = Router(name=__name__)


@start_router.message(
    MagicData(F.user),
    CommandStart(deep_link=True, deep_link_encoded=True, ignore_case=False),
    MagicData(F.command.args.regexp(INVITE_LINK_ID_REGEX)),
    MagicData(F.command.args.cast(UUID).as_("invite_id")),
)
async def start_with_invite_link(
    message: Message,
    state: FSMContext,
    member_service: MemberService,
    invite_id: UUID,
) -> None:
    travel = await member_service.use_invite_link(message.from_user.id, invite_id)
    if travel:
        text = TRAVEL_JOINED.format(title=travel.title)
        keyboard = check_joined_travel(travel.id, travel.title)
    else:
        text = BAD_INVITE_LINK
        keyboard = start_keyboard
    await message.answer(text=text, reply_markup=keyboard)
    await state.clear()


@start_router.message(CommandStart(), MagicData(F.user))
async def start_command_known(message: Message, state: FSMContext) -> None:
    text = START_TEXT
    await message.answer(text=text, reply_markup=start_keyboard)
    await state.clear()


@start_router.message(CommandStart())
async def start_command_unknown(message: Message) -> None:
    text = START_TEXT + "\n\n" + NEW_USER_TEXT
    await message.answer(text=text, reply_markup=fill_profile_keyboard)


@start_router.message(Command("help"), MagicData(F.user))
async def help_command_known(message: Message) -> None:
    text = HELP_TEXT
    await message.answer(text=text, reply_markup=start_keyboard)


@start_router.message(Command("help"))
async def help_command_unknown(message: Message) -> None:
    text = HELP_TEXT + "\n\n" + NEW_USER_TEXT
    await message.answer(text=text, reply_markup=fill_profile_keyboard)


@start_router.callback_query(OpenMenu.filter(F.menu == BotMenu.START))
async def start_callback(callback: CallbackQuery, state: FSMContext) -> None:
    text = START_TEXT
    await callback.message.edit_text(text=text, reply_markup=start_keyboard)
    await state.clear()
