from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.notes import (
    AddNoteData,
    DeleteNoteData,
    GetNoteData,
    NotesPaginator,
    NoteVisibilityData,
)
from bot.keyboards.paginate import paginate_keyboard
from bot.keyboards.universal import cancel_button
from bot.utils.enums import BotMenu
from core.models import Note, Travel
from core.service.notes import NoteService

choose_visibility_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Публичная",
                callback_data=NoteVisibilityData(is_public=True).pack(),
            ),
            InlineKeyboardButton(
                text="Приватная",
                callback_data=NoteVisibilityData(is_public=False).pack(),
            ),
        ],
        [cancel_button],
    ]
)


async def notes_keyboard(
    tg_id: int,
    page: int,
    travel_id: int,
    note_service: NoteService,
) -> InlineKeyboardMarkup:
    rows, width = 6, 1
    subjects = [
        InlineKeyboardButton(
            text=note.title,
            callback_data=GetNoteData(
                note_id=note.id,
                travel_id=travel_id,
                page=page,
            ).pack(),
        )
        for note in await note_service.list_with_access_check(tg_id, travel_id)
    ]

    create_note_button = InlineKeyboardButton(
        text="Добавить заметку",
        callback_data=AddNoteData(page=page, travel_id=travel_id).pack(),
    )

    return paginate_keyboard(
        buttons=subjects,
        menu=BotMenu.NOTES,
        page=page,
        rows=rows,
        width=width,
        additional_buttons=[create_note_button],
    )


def one_note_keyboard(
    note: Note,
    travel: Travel,
    tg_id: int,
    page: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if tg_id == note.creator_id or tg_id == travel.owner_id:
        builder.row(
            InlineKeyboardButton(
                text="Удалить",
                callback_data=DeleteNoteData(
                    note_id=note.id,
                    page=page,
                ).pack(),
            ),
            InlineKeyboardButton(
                text="Удалить",
                callback_data=DeleteNoteData(
                    note_id=note.id,
                    page=page,
                ).pack(),
            ),
        )

    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=NotesPaginator(
                menu=BotMenu.NOTES,
                page=page,
                travel_id=travel.id,
            ).pack(),
        )
    )

    return builder.as_markup()
