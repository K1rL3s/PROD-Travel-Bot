from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.notes import AddNoteData, NoteStatusData
from bot.callbacks.state import InStateData
from bot.filters.note import NoteDocumentFilter
from bot.filters.travel import TravelCallbackAccess, TravelStateAccess
from bot.handlers.notes.phrases import TITLE_ERROR
from bot.keyboards.notes import choose_status_keyboard, notes_keyboard
from bot.keyboards.universal import cancel_keyboard
from bot.utils.enums import Action
from bot.utils.states import NoteCreating
from bot.utils.tg import delete_last_message
from core.models import Note, TravelExtended
from core.service.notes import NoteService

router = Router(name=__name__)


@router.callback_query(AddNoteData.filter(), TravelCallbackAccess())
async def create_note(
    callback: CallbackQuery,
    callback_data: AddNoteData,
    state: FSMContext,
) -> None:
    text = "Придумайте короткое название для заметки, чтобы запомнить её"
    await callback.message.edit_text(text=text, reply_markup=cancel_keyboard)
    await state.set_state(NoteCreating.title)
    await state.set_data(
        {"travel_id": callback_data.travel_id, "last_id": callback.message.message_id}
    )


@router.message(F.text, NoteCreating.title)
async def create_note_title(
    message: Message,
    bot: Bot,
    state: FSMContext,
    note_service: NoteService,
) -> None:
    if (title := await NoteService.validate_title(note_service, message.text)) is None:
        await message.reply(text=TITLE_ERROR, reply_markup=cancel_keyboard)
        await delete_last_message(bot, state, message)
        return

    text = (
        "Сделать заметку публичной (для всех в путешествии) "
        "или приватной (только для вас)?"
    )
    bot_msg = await message.answer(text=text, reply_markup=choose_status_keyboard)

    await delete_last_message(bot, state, message)
    await state.update_data(title=title, last_id=bot_msg.message_id)
    await state.set_state(NoteCreating.status)


@router.callback_query(NoteStatusData.filter(), NoteCreating.status)
async def create_note_status(
    callback: CallbackQuery,
    callback_data: NoteStatusData,
    state: FSMContext,
) -> None:
    text = (
        "Отправьте мне текст, голосовоое соообщение, кружочек, фотографию, "
        "видео или документ. Я сохраню это как заметку."
    )
    await callback.message.edit_text(text=text, reply_markup=cancel_keyboard)

    await state.set_state(NoteCreating.file)
    await state.update_data(is_public=callback_data.is_public)


@router.message(NoteCreating.file, NoteDocumentFilter())
async def create_note_file(
    message: Message,
    state: FSMContext,
    bot: Bot,
    note_service: NoteService,
    document_id: str,
) -> None:
    data = await state.get_data()
    travel_id: int = data["travel_id"]
    title: str = data["title"]
    is_public: bool = data["is_public"]

    note = Note(
        title=title,
        travel_id=travel_id,
        creator_id=message.from_user.id,
        is_public=is_public,
        document_id=document_id,
    )
    await note_service.create_with_access_check(message.from_user.id, note)

    text = "Успешно сохранил"
    keyboard = await notes_keyboard(
        message.from_user.id,
        0,
        travel_id,
        note_service,
    )
    await message.answer(text=text, reply_markup=keyboard)

    await delete_last_message(bot, state, message)
    await state.clear()


@router.message(NoteCreating.file)
async def create_note_file_unknown(
    message: Message,
    state: FSMContext,
    bot: Bot,
) -> None:
    text = (
        "Такие файлы я ещё не умею сохранять. :(\n"
        "Вы можете загрузить текст, голосовоое соообщение, кружочек, фотографию, "
        "видео или документ"
    )
    await message.reply(text=text, reply_markup=None)

    await delete_last_message(bot, state, message)


@router.callback_query(
    InStateData.filter(F.action == Action.CANCEL),
    StateFilter(NoteCreating),
    TravelStateAccess(),
)
async def cancel_create_note(
    callback: CallbackQuery,
    state: FSMContext,
    travel: TravelExtended,
    note_service: NoteService,
) -> None:
    text = f'Заметки путешествия "{travel.title}"'
    keyboard = await notes_keyboard(
        callback.from_user.id,
        0,
        travel.id,
        note_service,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)

    await state.clear()
