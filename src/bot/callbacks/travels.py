from aiogram.filters.callback_data import CallbackData


class GetTravelData(CallbackData, prefix="get_travel"):
    travel_id: int
    page: int | None = None


class AddTravelData(CallbackData, prefix="add_travel"):
    page: int | None = None


class EditTravelData(CallbackData, prefix="edit_travel"):
    travel_id: int
    field: str | None = None
    page: int | None = None


class DeleteTravelData(CallbackData, prefix="delete_travel"):
    travel_id: int
    page: int | None = None
    sure: bool = False
