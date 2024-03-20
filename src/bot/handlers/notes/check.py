from aiogram import Bot, Router
from aiogram.types import CallbackQuery

from bot.callbacks import GetNoteData, NotesPaginator
from bot.filters import NoteCallbackAccess, TravelCallbackAccess
from bot.keyboards import notes_keyboard, one_note_keyboard
from core.models import NoteExtended, TravelExtended
from core.services import NoteService

router = Router(name=__name__)


@router.callback_query(NotesPaginator.filter(), TravelCallbackAccess())
async def paginate_notes(
    callback: CallbackQuery,
    callback_data: NotesPaginator,
    travel: TravelExtended,
    note_service: NoteService,
) -> None:
    text = f'Заметки путешествия "{travel.title}"'
    keyboard = await notes_keyboard(
        callback.from_user.id,
        callback_data.page,
        travel.id,
        note_service,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(
    GetNoteData.filter(),
    TravelCallbackAccess(),
    NoteCallbackAccess(),
)
async def one_note(
    callback: CallbackQuery,
    callback_data: GetNoteData,
    bot: Bot,
    note: NoteExtended,
    travel: TravelExtended,
) -> None:
    caption = "Вот файл с заметкой"
    text = "Действия"
    keyboard = one_note_keyboard(
        note,
        travel,
        callback.from_user.id,
        callback_data.page,
    )
    bot_msg = await bot.send_document(
        chat_id=callback.message.chat.id,
        document=note.document_id,
        caption=caption,
    )
    await bot_msg.reply(text=text, reply_markup=keyboard)
