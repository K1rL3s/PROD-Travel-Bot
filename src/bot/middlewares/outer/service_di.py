from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from core.service.location import LocationService
from core.service.notes import NoteService
from core.service.travel import TravelService
from core.service.user import UserService
from database.repositories import (
    LocationAlchemyRepo,
    NoteAlchemyRepo,
    TravelAlchemyRepo,
    UserAlchemyRepo,
)


class ServiceDIMiddleware(BaseMiddleware):
    """Мидлварь для добавления сервисов в контекст обработчиков телеграма."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        session: AsyncSession = data["session"]

        user_repo = UserAlchemyRepo(session)
        location_repo = LocationAlchemyRepo(session)
        note_repo = NoteAlchemyRepo(session)
        travel_repo = TravelAlchemyRepo(session)

        user_service = UserService(user_repo)
        location_service = LocationService(location_repo)
        note_service = NoteService(note_repo)
        travel_service = TravelService(travel_repo)

        data.update(
            {
                "user_service": user_service,
                "location_service": location_service,
                "note_service": note_service,
                "travel_service": travel_service,
            }
        )

        return await handler(event, data)
