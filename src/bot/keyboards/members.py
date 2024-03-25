from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks import (
    AddMemberData,
    DeleteMemberData,
    GetMemberData,
    GetTravelData,
    MembersPaginator,
)
from bot.keyboards.emoji import ADD, BACK, DELETE, TRAVEL
from bot.keyboards.paginate import paginate_keyboard
from bot.utils.enums import BotMenu
from core.models import Travel, User
from core.services import MemberService


async def members_keyboard(
    tg_id: int,
    page: int,
    travel: Travel,
    member_service: MemberService,
) -> InlineKeyboardMarkup:
    rows, width = 6, 1
    subjects = [
        InlineKeyboardButton(
            text=f"{member.name}",
            callback_data=GetMemberData(
                member_id=member.id,
                travel_id=travel.id,
                page=page,
            ).pack(),
        )
        for member in await member_service.list_with_access_check(tg_id, travel.id)
    ]

    additional_buttons = [
        InlineKeyboardButton(
            text=f"{BACK}{TRAVEL} Путешествие",
            callback_data=GetTravelData(travel_id=travel.id).pack(),
        )
    ]
    if travel.owner_id == tg_id:
        additional_buttons.append(
            InlineKeyboardButton(
                text=f"{ADD} Пригласить",
                callback_data=AddMemberData(page=page, travel_id=travel.id).pack(),
            )
        )

    return paginate_keyboard(
        buttons=subjects,
        menu=BotMenu.MEMBERS,
        page=page,
        rows=rows,
        width=width,
        additional_buttons=additional_buttons,
        fabric=MembersPaginator,
        travel_id=travel.id,
    )


def one_member_keyboard(
    member: User,
    travel: Travel,
    tg_id: int,
    page: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if tg_id == travel.owner_id and tg_id != member.id:
        builder.row(
            InlineKeyboardButton(
                text=f"{DELETE} Удалить",
                callback_data=DeleteMemberData(
                    member_id=member.id,
                    travel_id=travel.id,
                    page=page,
                ).pack(),
            )
        )

    builder.row(
        InlineKeyboardButton(
            text=f"{BACK} Все друзья",
            callback_data=MembersPaginator(page=page, travel_id=travel.id).pack(),
        ),
        InlineKeyboardButton(
            text=f"{TRAVEL} Путешествие",
            callback_data=GetTravelData(page=0, travel_id=travel.id).pack(),
        ),
    )

    return builder.as_markup()


def delete_member_keyboard(
    travel_id: int,
    member_id: int,
    page: int,
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{BACK} Назад",
                    callback_data=GetMemberData(
                        travel_id=travel_id,
                        member_id=member_id,
                        page=page,
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text=f"{DELETE} Удалить",
                    callback_data=DeleteMemberData(
                        travel_id=travel_id,
                        member_id=member_id,
                        page=page,
                        sure=True,
                    ).pack(),
                ),
            ],
        ]
    )
