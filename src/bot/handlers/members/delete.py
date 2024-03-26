from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callbacks import DeleteMemberData
from bot.filters import MemberCallbackDI, TravelCallbackOwner
from bot.keyboards import delete_member_keyboard, members_keyboard
from core.models import TravelExtended, User
from core.services import MemberService

from .phrases import ALL_MEMBERS

router = Router(name=__name__)


@router.callback_query(
    DeleteMemberData.filter(F.sure.is_(False)),
    TravelCallbackOwner(),
    MemberCallbackDI(),
)
async def delete_member(
    callback: CallbackQuery,
    callback_data: DeleteMemberData,
    travel: TravelExtended,
    member: User,
) -> None:
    text = (
        f'❓ Ты уверен, что хочешь удалить участника "{member.name}" '
        f'из путешествия "{travel.title}"?'
    )
    keyboard = delete_member_keyboard(
        callback_data.travel_id, member.id, callback_data.page
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(
    DeleteMemberData.filter(F.sure.is_(True)),
    TravelCallbackOwner(),
    MemberCallbackDI(),
)
async def delete_member_sure(
    callback: CallbackQuery,
    callback_data: DeleteMemberData,
    state: FSMContext,
    travel: TravelExtended,
    member: User,
    member_service: MemberService,
) -> None:
    await member_service.delete_with_access_check(
        callback.from_user.id,
        member.id,
        travel.id,
    )

    text = ALL_MEMBERS.format(title=travel.title)
    keyboard = await members_keyboard(
        callback.from_user.id,
        callback_data.page,
        travel,
        member_service,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)

    await state.clear()
