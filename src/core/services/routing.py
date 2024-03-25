from core.geo import Routing
from core.models import TravelExtended
from core.repositories import LocationRepo
from core.services.base import BaseService


class RoutingService(BaseService):
    def __init__(self, rounting: Routing, location_repo: LocationRepo) -> None:
        self.rounting = rounting
        self.location_repo = location_repo

    async def get_route(self, travel: TravelExtended) -> tuple[str, bytes | None]:
        locations = await self.location_repo.list_by_travel_id(travel.id)
        url = self.rounting.route_url(
            [(loc.latitude, loc.longitude) for loc in locations]
        )
        image = await self.rounting.route_image(
            [(loc.longitude, loc.latitude) for loc in locations]
        )
        return url, image
