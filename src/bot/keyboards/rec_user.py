from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks import (
    AddRecommendUser,
    GetRecommendUser,
    GetTravelData,
    RecommendPaginator,
)
from bot.keyboards.emoji import BACK, INVITE, TRAVEL
from bot.keyboards.paginate import paginate_keyboard
from bot.utils.enums import BotMenu
from core.services import MemberService


async def recommend_users_keyboard(
    tg_id: int,
    travel_id: int,
    page: int,
    member_service: MemberService,
) -> InlineKeyboardMarkup:
    rows, width = 6, 1
    subjects = [
        InlineKeyboardButton(
            text=f"{member.name}",
            callback_data=GetRecommendUser(
                user_id=member.id,
                travel_id=travel_id,
                page=page,
            ).pack(),
        )
        for member in await member_service.get_recommended_users_with_access_check(
            tg_id,
            travel_id,
        )
    ]

    additional_buttons = [
        InlineKeyboardButton(
            text=f"{BACK}{TRAVEL} Путешествие",
            callback_data=GetTravelData(travel_id=travel_id).pack(),
        )
    ]

    return paginate_keyboard(
        buttons=subjects,
        menu=BotMenu.RECOMMEND_USERS,
        page=page,
        rows=rows,
        width=width,
        additional_buttons=additional_buttons,
        fabric=RecommendPaginator,
        travel_id=travel_id,
    )


def one_recommend_user_keyboard(
    recommend_user_id: int,
    travel_id: int,
    page: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=f"{BACK} Все рекомендации",
            callback_data=RecommendPaginator(page=page, travel_id=travel_id).pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f"{INVITE} Пригласить",
            callback_data=AddRecommendUser(
                user_id=recommend_user_id,
                travel_id=travel_id,
                page=page,
            ).pack(),
        )
    )

    return builder.as_markup()
