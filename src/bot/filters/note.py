from typing import Any

from bot.filters.access import CallbackAccess, StateAccess
from core.models import NoteExtended


def _check_callback_data(callback_data: Any) -> int | None:
    if hasattr(callback_data, "note_id") and isinstance(callback_data.note_id, int):
        return callback_data.note_id
    return None


class NoteCallbackAccess(CallbackAccess[NoteExtended, int]):
    def __init__(self) -> None:
        super().__init__(
            service_context_var="note_service",
            add_context_var="note",
            callback_data_checker=_check_callback_data,
            owner_mode=False,
        )


class NoteCallbackOwner(CallbackAccess[NoteExtended, int]):
    def __init__(self) -> None:
        super().__init__(
            service_context_var="note_service",
            add_context_var="note",
            callback_data_checker=_check_callback_data,
            owner_mode=True,
        )


class NoteStateAccess(StateAccess[NoteExtended, int]):
    def __init__(self) -> None:
        super().__init__(
            service_context_var="note_service",
            add_context_var="note",
            state_key="note_id",
            owner_mode=False,
        )


class NoteStateOwner(StateAccess[NoteExtended, int]):
    def __init__(self) -> None:
        super().__init__(
            service_context_var="note_service",
            add_context_var="note",
            state_key="note_id",
            owner_mode=False,
        )
