from core.repositories.abc import TravelRepo


class TravelService:
    def __init__(self, travel_repo: TravelRepo) -> None:
        self.travel_repo = travel_repo
