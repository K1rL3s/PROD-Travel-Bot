from core.geo import Routing

GRAPHHOPPER_URL = "https://graphhopper.com/maps/"
PROJECT_OSRM_URL = "https://map.project-osrm.org/"


class GraphHopperRouting(Routing):
    def route_url(self, points: list[tuple[float, float]]) -> str:
        return (
            f"{GRAPHHOPPER_URL}?point="
            f"{'&point='.join(f'{lat},{lon}' for lat, lon in points)}"
        )


class OSRMRouting(Routing):
    def route_url(self, points: list[tuple[float, float]]) -> str:
        return (
            f"{PROJECT_OSRM_URL}?loc="
            f"{'&loc='.join(f'{lat},{lon}' for lat, lon in points)}&hl=ru&alt=0&srv=0"
        )


if __name__ == "__main__":
    # graph = OSRMRouting()
    graph = GraphHopperRouting()
    print(
        graph.route_url(
            [
                (60.939187, 76.551179),
                (61.003445, 69.019001),
                (56.839104, 60.60825),
                (55.750541, 37.617478),
            ]
        )
    )
