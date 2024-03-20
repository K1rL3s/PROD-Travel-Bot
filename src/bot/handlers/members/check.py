from aiogram import Router
from aiogram.types import CallbackQuery

from bot.callbacks import GetMemberData, MembersPaginator
from bot.filters import MemberCallbackDI, TravelCallbackAccess
from bot.keyboards import members_keyboard, one_member_keyboard
from core.models import TravelExtended, User
from core.services import MemberService

from .funcs import format_member

router = Router(name=__name__)


@router.callback_query(MembersPaginator.filter(), TravelCallbackAccess())
async def members_paginator(
    callback: CallbackQuery,
    callback_data: MembersPaginator,
    travel: TravelExtended,
    member_service: MemberService,
) -> None:
    text = f'Участники путешествия "{travel.title}"'
    keyboard = await members_keyboard(
        callback.from_user.id,
        callback_data.page,
        travel,
        member_service,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(
    GetMemberData.filter(),
    TravelCallbackAccess(),
    MemberCallbackDI(),
)
async def one_note(
    callback: CallbackQuery,
    callback_data: GetMemberData,
    member: User,
    travel: TravelExtended,
) -> None:
    text = format_member(member)
    keyboard = one_member_keyboard(
        member,
        travel,
        callback.from_user.id,
        callback_data.page,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)
