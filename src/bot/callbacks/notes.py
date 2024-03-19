from aiogram.filters.callback_data import CallbackData

from bot.callbacks.paginate import Paginator
from bot.utils.enums import BotMenu


class NotesPaginator(Paginator, prefix="notes_paginator"):
    menu: str = BotMenu.NOTES
    travel_id: int


class GetNoteData(CallbackData, prefix="get_note"):
    note_id: int
    travel_id: int
    page: int


class AddNoteData(CallbackData, prefix="add_note"):
    travel_id: int
    page: int


class SwitchNoteData(CallbackData, prefix="switch_note"):
    note_id: int
    page: int


class DeleteNoteData(CallbackData, prefix="delete_note"):
    note_id: int
    page: int


class NoteStatusData(CallbackData, prefix="note_status"):
    is_public: bool
