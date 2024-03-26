from aiogram.filters.callback_data import CallbackData


class GetTravelData(CallbackData, prefix="get_travel"):
    travel_id: int
    page: int = 0


class AddTravelData(CallbackData, prefix="add_travel"):
    page: int = 0


class EditTravelData(CallbackData, prefix="edit_travel"):
    travel_id: int
    field: str | None = None
    page: int = 0


class DeleteTravelData(CallbackData, prefix="delete_travel"):
    travel_id: int
    page: int = 0
    sure: bool = False


class GetRouteData(CallbackData, prefix="get_router"):
    travel_id: int
    page: int = 0


class LeaveTravelData(CallbackData, prefix="leave_travel"):
    travel_id: int
    page: int = 0
    sure: bool = False
