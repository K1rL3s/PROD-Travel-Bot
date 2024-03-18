from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.notes import AddNoteData, NoteVisibilityData
from bot.callbacks.state import InStateData
from bot.filters.travel import TravelCallbackAccess
from bot.keyboards.notes import choose_visibility_keyboard
from bot.keyboards.universal import cancel_keyboard
from bot.utils.enums import Action
from bot.utils.states import NoteCreating
from bot.utils.tg import delete_last_message
from core.models import Note
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
) -> None:
    text = (
        "Сделать заметку публичной (для всех в путешествии) "
        "или приватной (только для вас)?"
    )
    bot_msg = await message.answer(text=text, reply_markup=choose_visibility_keyboard)

    await delete_last_message(bot, state, message)
    await state.update_data(title=message.text, last_id=bot_msg.message_id)
    await state.set_state(NoteCreating.visibility)


@router.callback_query(NoteVisibilityData.filter(), NoteCreating.visibility)
async def create_note_visibility(
    callback: CallbackQuery,
    callback_data: NoteVisibilityData,
    state: FSMContext,
) -> None:
    text = "Отправьте мне файл, изображение или текст. Я сохраню это как заметку."
    await callback.message.edit_text(text=text, reply_markup=cancel_keyboard)

    await state.set_state(NoteCreating.file)
    await state.update_data(is_public=callback_data.is_public)


@router.message(NoteCreating.file, F.text, F.text.as_("text"))
@router.message(NoteCreating.file, F.photo.F.photo[-1].file_id.as_("photo_id"))
@router.message(NoteCreating.file, F.document, F.documnt.file_id.as_("document_id"))
async def create_note_file(
    message: Message,
    state: FSMContext,
    bot: Bot,
    note_service: NoteService,
    text: str | None = None,
    photo_id: str | None = None,
    document_id: str | None = None,
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
    await message.answer(text=text, reply_markup=None)

    await state.clear()
    await delete_last_message(bot, state, message)


@router.callback_query(
    InStateData.filter(F.action == Action.CANCEL),
    StateFilter(NoteCreating),
)
async def cancel_create_note(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(text="ok")
    await state.clear()
