from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.callbacks import InStateData, OpenMenu, ProfileData
from bot.keyboards import edit_profile_keyboard
from bot.utils.enums import Action, BotMenu, SlashCommand
from bot.utils.format import format_user
from bot.utils.states import ProfileState
from core.models import UserExtended

router = Router(name=__name__)


@router.callback_query(ProfileData.filter(F.action == Action.GET))
@router.callback_query(OpenMenu.filter(F.menu == BotMenu.PROFILE))
@router.callback_query(
    InStateData.filter(F.action == Action.CANCEL),
    ProfileState.editing,
)
async def check_my_profile_callback(
    callback: CallbackQuery,
    user: UserExtended,
) -> None:
    await callback.message.edit_text(
        text=format_user(user),
        reply_markup=edit_profile_keyboard,
    )


@router.message(Command(SlashCommand.PROFILE))
async def check_my_profile_message(
    message: Message,
    user: UserExtended,
) -> None:
    await message.answer(
        text=format_user(user),
        reply_markup=edit_profile_keyboard,
    )
