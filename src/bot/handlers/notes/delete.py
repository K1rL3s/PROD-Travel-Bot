from aiogram import Router
from aiogram.types import CallbackQuery

from bot.callbacks import DeleteNoteData
from bot.filters import NoteCallbackOwner
from bot.keyboards import notes_keyboard
from core.models import NoteExtended
from core.services import NoteService

from .phrases import ALL_NOTES

router = Router(name=__name__)


@router.callback_query(
    DeleteNoteData.filter(),
    NoteCallbackOwner(),
)
async def delete_note(
    callback: CallbackQuery,
    callback_data: DeleteNoteData,
    note: NoteExtended,
    note_service: NoteService,
) -> None:
    await note_service.delete_with_access_check(callback.from_user.id, note.id)

    text = ALL_NOTES.format(title=note.travel.title)
    keyboard = await notes_keyboard(
        callback.from_user.id,
        callback_data.page,
        note.travel_id,
        note_service,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)
