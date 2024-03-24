from core.geo import Routing
from core.models import TravelExtended
from core.repositories import LocationRepo
from core.services.base import BaseService


class RoutingService(BaseService):
    def __init__(self, rounting: Routing, location_repo: LocationRepo) -> None:
        self.rounting = rounting
        self.location_repo = location_repo

    async def get_route_url(self, travel: TravelExtended) -> str:
        locations = [travel.owner.city]
        locations.extend(await self.location_repo.list_by_travel_id(travel.id))
        return self.rounting.route_url(
            [(loc.latitude, loc.longitude) for loc in locations]
        )
