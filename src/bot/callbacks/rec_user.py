from aiogram.filters.callback_data import CallbackData

from bot.callbacks import Paginator
from bot.utils.enums import BotMenu


class RecommendPaginator(Paginator, prefix="rec_paginator"):
    menu: str = BotMenu.RECOMMEND_USERS
    travel_id: int


class GetRecommendUser(CallbackData, prefix="get_rec_user"):
    user_id: int
    travel_id: int
    page: int


class AddRecommendUser(CallbackData, prefix="add_rec_user"):
    user_id: int
    travel_id: int
    page: int
