from typing import cast

from aiogram import Bot, Router
from aiogram.types import CallbackQuery

from bot.callbacks import GetRecommendUser, RecommendPaginator
from bot.callbacks.rec_user import AddRecommendUser
from bot.filters import TravelCallbackOwner
from bot.keyboards import one_recommend_user_keyboard, recommend_users_keyboard
from bot.utils.format import format_invite_link, format_member
from core.models import InviteLinkExtended, Travel, User
from core.services import MemberService, UserService

from .phrases import RECOMMENDED_USERS

router = Router(name=__name__)


@router.callback_query(RecommendPaginator.filter(), TravelCallbackOwner())
async def get_recommend_users(
    callback: CallbackQuery,
    callback_data: RecommendPaginator,
    member_service: MemberService,
    user: User,
    travel: Travel,
) -> None:
    text = RECOMMENDED_USERS
    keyboard = await recommend_users_keyboard(
        user.id,
        travel.id,
        callback_data.page,
        member_service,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(GetRecommendUser.filter(), TravelCallbackOwner())
async def get_one_recommend_user(
    callback: CallbackQuery,
    callback_data: GetRecommendUser,
    user_service: UserService,
    travel: Travel,
) -> None:
    member = await user_service.get(callback_data.user_id)
    text = "👇 Вот, кого я нашёл для тебя\n\n" + format_member(member)
    keyboard = one_recommend_user_keyboard(
        member.id,
        travel.id,
        callback_data.page,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(AddRecommendUser.filter(), TravelCallbackOwner())
async def inivte_recommend_user(
    callback: CallbackQuery,
    callback_data: GetRecommendUser,
    bot: Bot,
    member_service: MemberService,
    user: User,
    travel: Travel,
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

    text = RECOMMENDED_USERS
    keyboard = await recommend_users_keyboard(
        user.id,
        travel.id,
        callback_data.page,
        member_service,
    )
    await callback.message.answer(text=text, reply_markup=keyboard)
