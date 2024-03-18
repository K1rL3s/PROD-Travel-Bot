from aiogram.filters.callback_data import CallbackData

from bot.callbacks.paginate import Paginator


class NotesPaginator(Paginator, prefix="notes_paginator"):
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


class NoteVisibilityData(CallbackData, prefix="note_visibility"):
    is_public: bool
