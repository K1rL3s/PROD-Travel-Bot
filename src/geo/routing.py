from pathlib import Path

from aiohttp import ClientSession

from core.geo import Routing

GRAPHHOPPER_URL = "https://graphhopper.com/maps/"
ICON_PATH = Path(__file__).parent.resolve() / "icon.png"


class GraphHopperRouting(Routing):
    def __init__(
        self,
        session: ClientSession,
        route_host: str,
        route_port: int,
    ) -> None:
        self.session = session
        self.url = f"http://{route_host}:{route_port}/route"

    def route_url(self, points: list[tuple[float, float]]) -> str:
        return (
            f"{GRAPHHOPPER_URL}?point="
            f"{'&point='.join(f'{lat},{lon}' for lat, lon in points)}"
        )

    async def route_image(
        self,
        points_lon_lat: list[tuple[float, float]],
    ) -> bytes | None:
        body = {"points": points_lon_lat}
        headers = {"Content-Type": "application/json"}

        async with self.session.post(
            self.url,
            json=body,
            headers=headers,
        ) as resp:
            if resp.status != 200:
                return None
            return await resp.read()


async def main() -> None:
    import aiohttp

    async with aiohttp.ClientSession() as session:
        graph = GraphHopperRouting(
            session,
            "127.0.0.1",
            5123,
        )
        # print(
        #     graph.route_url(
        #         [
        #             (60.939187, 76.551179),
        #             (61.003445, 69.019001),
        #             (56.839104, 60.60825),
        #             (55.750541, 37.617478),
        #         ]
        #     )
        # )
        bytes_io = await graph.route_image(
            [
                (76.551179, 60.939187),
                (69.019001, 61.003445),
                (60.60825, 56.839104),
                (37.617478, 55.750541),
            ]
        )
        print(len(bytes_io.read()))


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
