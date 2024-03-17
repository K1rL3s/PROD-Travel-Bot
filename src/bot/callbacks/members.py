from aiogram.filters.callback_data import CallbackData


class MemberCRUD(CallbackData, prefix="members"):
    action: str
    travel_id: int
