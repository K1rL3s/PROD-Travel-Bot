from aiogram.filters.callback_data import CallbackData

from bot.callbacks.paginate import Paginator
from bot.utils.enums import BotMenu


class MembersPaginator(Paginator, prefix="members_paginator"):
    menu: str = BotMenu.MEMBERS
    travel_id: int


class GetMemberData(CallbackData, prefix="get_member"):
    member_id: int
    travel_id: int
    page: int


class AddMemberData(CallbackData, prefix="add_member"):
    travel_id: int
    page: int


class DeleteMemberData(CallbackData, prefix="delete_member"):
    member_id: int
    travel_id: int
    page: int
    sure: bool = False
