from aiogram.filters.callback_data import CallbackData


class NoteCRUD(CallbackData, prefix="note"):
    action: str
    travel_id: int
