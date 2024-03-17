from aiogram.filters.callback_data import CallbackData


class TravelCRUD(CallbackData, prefix="travels"):
    action: str
    id: int | None = None
    page: int | None = None


class EditTravelData(CallbackData, prefix="edit_travel"):
    id: int
    field: str
    page: int


class DeleteTravelData(CallbackData, prefix="delete_travel"):
    id: int
    page: int
