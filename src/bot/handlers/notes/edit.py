from aiogram import Router
from aiogram.types import CallbackQuery

from bot.callbacks.notes import SwitchNoteData
from bot.filters.note import NoteCallbackOwner
from bot.keyboards.notes import one_note_keyboard
from core.models import NoteExtended
from core.service.notes import NoteService

router = Router(name=__name__)


@router.callback_query(SwitchNoteData.filter(), NoteCallbackOwner())
async def switch_note_status(
    callback: CallbackQuery,
    callback_data: SwitchNoteData,
    note: NoteExtended,
    note_service: NoteService,
) -> None:
    note = await note_service.switch_status_with_access_check(
        callback.from_user.id, note.id
    )

    text = f'Заметка "{note.title}" путешествия "{note.travel.title}"'
    keyboard = one_note_keyboard(
        note,
        note.travel,
        callback.from_user.id,
        callback_data.page,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)
