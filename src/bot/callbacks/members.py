from aiogram.filters.callback_data import CallbackData


class MemberCRUD(CallbackData, prefix="member"):
    action: str
    travel_id: int
