from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from geopy import Nominatim
from geopy.adapters import AioHTTPAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from core.service.geo import GeoService
from core.service.location import LocationService
from core.service.member import MemberService
from core.service.note import NoteService
from core.service.travel import TravelService
from core.service.user import UserService
from database.repositories import (
    InviteLinkAlchemyRepo,
    LocationAlchemyRepo,
    MemberAlchemyRepo,
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
        travel_repo = TravelAlchemyRepo(session)
        location_repo = LocationAlchemyRepo(session)
        note_repo = NoteAlchemyRepo(session)
        member_repo = MemberAlchemyRepo(session)
        invite_link_repo = InviteLinkAlchemyRepo(session)

        user_service = UserService(user_repo)
        travel_service = TravelService(travel_repo)
        location_service = LocationService(location_repo, travel_repo)
        note_service = NoteService(note_repo, travel_repo)
        member_service = MemberService(member_repo, travel_repo, invite_link_repo)

        async with Nominatim(
            timeout=10,
            user_agent="travel-k1rl3s-bot-application",
            adapter_factory=AioHTTPAdapter,
        ) as geolocator:
            geo_service = GeoService(geolocator)

            data.update(
                {
                    "user_service": user_service,
                    "travel_service": travel_service,
                    "location_service": location_service,
                    "note_service": note_service,
                    "member_service": member_service,
                    "geo_service": geo_service,
                }
            )

            return await handler(event, data)
