from aiogram.filters.callback_data import CallbackData


class OpenMenu(CallbackData, prefix="open_menu"):
    menu: str
    page: int = 0
