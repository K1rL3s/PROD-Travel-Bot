from aiogram.filters.callback_data import CallbackData


class GetTravelData(CallbackData, prefix="get_travel"):
    travel_id: int
    page: int | None = None


class AddTravelData(CallbackData, prefix="add_travel"):
    page: int


class EditTravelData(CallbackData, prefix="edit_travel"):
    travel_id: int
    field: str
    page: int | None = None


class DeleteTravelData(CallbackData, prefix="delete_travel"):
    travel_id: int
    page: int | None = None
