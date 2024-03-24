from aiogram.filters.callback_data import CallbackData

from bot.callbacks.paginate import Paginator
from bot.utils.enums import BotMenu


class LocationsPaginator(Paginator, prefix="locations_paginator"):
    menu: str = BotMenu.LOCATIONS
    travel_id: int


class GetLocationData(CallbackData, prefix="get_location"):
    location_id: int
    page: int


class AddLocationData(CallbackData, prefix="add_location"):
    travel_id: int
    page: int


class EditLocationData(CallbackData, prefix="edit_location"):
    location_id: int
    field: str | None = None
    page: int


class DeleteLocationData(CallbackData, prefix="delete_location"):
    location_id: int
    page: int
    sure: bool = False


class GetWeatherData(CallbackData, prefix="get_weather"):
    location_id: int
    page: int
