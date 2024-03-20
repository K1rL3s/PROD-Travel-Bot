from typing import cast

from aiogram import Bot, Router
from aiogram.types import CallbackQuery

from bot.callbacks import AddMemberData
from bot.filters import TravelCallbackOwner
from bot.keyboards import members_keyboard
from core.models import InviteLinkExtended, TravelExtended
from core.services import MemberService

from .funcs import format_invite_link

router = Router(name=__name__)


@router.callback_query(AddMemberData.filter(), TravelCallbackOwner())
async def generate_invite_link(
    callback: CallbackQuery,
    callback_data: AddMemberData,
    bot: Bot,
    travel: TravelExtended,
    member_service: MemberService,
) -> None:
    invite_link = cast(
        InviteLinkExtended,
        await member_service.create_invite_link_with_access_check(
            callback.from_user.id,
            travel.id,
        ),
    )

    text = await format_invite_link(invite_link, bot)
    await callback.message.answer(text=text)

    text = f'Участники путешествия "{travel.title}"'
    keyboard = await members_keyboard(
        callback.from_user.id,
        callback_data.page,
        travel,
        member_service,
    )
    await callback.message.answer(text=text, reply_markup=keyboard)
    await callback.message.delete()
