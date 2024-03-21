from abc import ABC
from typing import Any
from uuid import uuid4

from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.types import BufferedInputFile, Message

from bot.filters.access import CallbackAccess, StateAccess
from core.models import NoteExtended


class NoteCallbackBase(CallbackAccess[NoteExtended, int], ABC):
    @staticmethod
    def _check_callback_data(callback_data: Any) -> int | None:
        if hasattr(callback_data, "note_id") and isinstance(callback_data.note_id, int):
            return callback_data.note_id
        return None


class NoteCallbackAccess(NoteCallbackBase):
    def __init__(self) -> None:
        super().__init__(
            service_context_var="note_service",
            add_context_var="note",
            owner_mode=False,
        )


class NoteCallbackOwner(NoteCallbackBase):
    def __init__(self) -> None:
        super().__init__(
            service_context_var="note_service",
            add_context_var="note",
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


class NoteDocumentFilter(BaseFilter):
    async def __call__(self, message: Message, bot: Bot) -> bool | dict[str, Any]:
        if message.document:
            return {"document_id": message.document.file_id}

        if message.photo:
            photo = await bot.download(message.photo[-1].file_id)
            document = BufferedInputFile(
                file=photo.read(),
                filename=str(uuid4()) + ".jpg",
            )
            bot_msg = await bot.send_document(
                chat_id=message.chat.id,
                document=document,
            )
            return {"document_id": bot_msg.document.file_id}

        if message.voice:
            return {"document_id": message.voice.file_id}

        if message.video_note:
            return {"document_id": message.video_note.file_id}

        if message.video:
            return {"document_id": message.video.file_id}

        if message.text:
            document = BufferedInputFile(
                file=message.text.encode("utf-8"),
                filename=str(uuid4()) + ".txt",
            )
            bot_msg = await bot.send_document(
                chat_id=message.chat.id,
                document=document,
            )
            return {"document_id": bot_msg.document.file_id}

        return False
