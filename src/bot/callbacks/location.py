from aiogram.filters.callback_data import CallbackData


class LocationCRUD(CallbackData, prefix="locations"):
    action: str
    travel_id: int
