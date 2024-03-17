from aiogram.filters.callback_data import CallbackData


class NoteCRUD(CallbackData, prefix="notes"):
    action: str
    travel_id: int
