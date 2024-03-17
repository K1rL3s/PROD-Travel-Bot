from collections.abc import Awaitable, Callable
from typing import Any, Final

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

SESSION_KEY: Final[str] = "session"


class DBSessionMiddleware(BaseMiddleware):
    """Мидлварь для добавления сессии в контекст обработчиков телеграма."""

    def __init__(
        self,
        session_maker: async_sessionmaker[AsyncSession],
        session_key: str = SESSION_KEY,
    ) -> None:
        self.session_maker = session_maker
        self.session_key = session_key

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with self.session_maker() as session:
            data[self.session_key] = session
            return await handler(event, data)
