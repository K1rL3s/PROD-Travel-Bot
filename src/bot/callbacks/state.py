from aiogram.filters.callback_data import CallbackData


class InStateData(CallbackData, prefix="in_state"):
    action: str
