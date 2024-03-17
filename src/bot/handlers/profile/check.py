from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.callbacks.menu import OpenMenu
from bot.callbacks.profile import ProfileData
from bot.callbacks.state import InStateData
from bot.keyboards.profile import edit_profile_keyboard
from bot.utils.enums import Action, BotMenu, SlashCommand, TextCommand
from bot.utils.states import ProfileState
from core.models import User

from .funcs import format_user_profile

router = Router(name=__name__)


@router.callback_query(ProfileData.filter(F.action == Action.GET))
@router.callback_query(OpenMenu.filter(F.menu == BotMenu.PROFILE))
@router.callback_query(
    InStateData.filter(F.action == Action.CANCEL),
    ProfileState.editing,
)
async def check_my_profile_callback(
    callback: CallbackQuery,
    user: User,
) -> None:
    await callback.message.edit_text(
        text=format_user_profile(user),
        reply_markup=edit_profile_keyboard,
    )


@router.message(F.text == TextCommand.PROFILE)
@router.message(Command(SlashCommand.PROFILE))
async def check_my_profile_message(
    message: Message,
    user: User,
) -> None:
    await message.answer(
        text=format_user_profile(user),
        reply_markup=edit_profile_keyboard,
    )
