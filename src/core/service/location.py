from core.repositories import LocationRepo


class LocationService:
    def __init__(self, location_repo: LocationRepo) -> None:
        self.location_repo = location_repo
