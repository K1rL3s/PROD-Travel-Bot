from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiohttp import ClientSession
from geopy.adapters import AioHTTPAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from core.services import (
    GeoService,
    LocationService,
    MemberService,
    NoteService,
    RoutingService,
    TravelService,
    UserService,
    WeatherService,
)
from database.repositories import (
    CityAlchemyRepo,
    CountryAlchemyRepo,
    InviteLinkAlchemyRepo,
    LocationAlchemyRepo,
    MemberAlchemyRepo,
    NoteAlchemyRepo,
    TravelAlchemyRepo,
    UserAlchemyRepo,
)
from geo import GeoPyLocator, GraphHopperRouting, OpenWeather, TzfTimezoner
from settings import Settings


class ServiceDIMiddleware(BaseMiddleware):
    """Мидлварь для добавления сервисов в контекст обработчиков телеграма."""

    def __init__(
        self,
        aiohttp_session: ClientSession,
        settings: Settings,
    ) -> None:
        self.aiohttp_session = aiohttp_session
        self.settings = settings

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
        country_repo = CountryAlchemyRepo(session)
        city_repo = CityAlchemyRepo(session)
        geo_weather = OpenWeather(
            self.aiohttp_session,
            self.settings.api.open_weather_key,
        )
        routing = GraphHopperRouting(
            self.aiohttp_session,
            self.settings.route.host,
            self.settings.route.port,
        )
        timezoner = TzfTimezoner()

        user_service = UserService(user_repo)
        travel_service = TravelService(travel_repo)
        location_service = LocationService(location_repo, travel_repo)
        note_service = NoteService(note_repo, travel_repo)
        member_service = MemberService(member_repo, travel_repo, invite_link_repo)
        weather_service = WeatherService(geo_weather)
        routing_service = RoutingService(routing, location_repo)

        async with GeoPyLocator(
            timeout=10,
            user_agent="travel-k1rl3s-bot-application",
            adapter_factory=AioHTTPAdapter,
        ) as geolocator:
            geo_service = GeoService(geolocator, timezoner, country_repo, city_repo)

            data.update(
                {
                    "user_service": user_service,
                    "travel_service": travel_service,
                    "location_service": location_service,
                    "note_service": note_service,
                    "member_service": member_service,
                    "geo_service": geo_service,
                    "weather_service": weather_service,
                    "routing_service": routing_service,
                }
            )

            return await handler(event, data)
