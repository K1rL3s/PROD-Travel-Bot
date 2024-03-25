import logging
import os
from io import BytesIO
from pathlib import Path

import requests
from flask import Flask, request, send_file
from staticmap import IconMarker, Line, StaticMap
from waitress import serve

app = Flask(__name__)

GRAPHHOPPER_API = "https://graphhopper.com/api/1/route"
ICON_PATH = Path(__file__).parent.resolve() / "icon.png"
API_KEY = os.environ["GRAPHHOPPER_KEY"]


class GraphHopperRouting:
    def route_image(self, points_lon_lat: list[tuple[float, float]]) -> BytesIO | None:
        params = {"key": API_KEY}
        body = {
            "locale": "ru",
            "optimize": "false",
            "instructions": False,
            "points_encoded": False,
            "points": points_lon_lat,
        }
        headers = {"Content-Type": "application/json"}

        resp = requests.post(GRAPHHOPPER_API, json=body, params=params, headers=headers)
        if resp.status_code != 200:
            return None
        data = resp.json()

        path = data["paths"][0]
        points = path["points"]["coordinates"]
        original_points = path["snapped_waypoints"]["coordinates"]

        return self.build_static_map(points, original_points)

    def build_static_map(
        self,
        points: list[tuple[int, int]],
        original_points: list[tuple[int, int]],
    ) -> BytesIO:
        static_map = StaticMap(1024, 1024, 20, 20)
        for i in range(len(points) - 1):
            curr = points[i]
            next_ = points[i + 1]
            static_map.add_line(Line([curr, next_], "blue", 3))
        for point in original_points:
            static_map.add_marker(IconMarker(point, ICON_PATH, 19, 57))
        render = static_map.render()

        output = BytesIO()
        render.save(output, format="PNG")
        output.seek(0)
        return output


@app.route("/route", methods=["POST"])
def get_route_image():
    data = request.json
    points = data.get("points")
    if not points or not isinstance(points, list):
        return "Неверный body", 400

    graph = GraphHopperRouting()
    buffered_image = graph.route_image(points)

    if not buffered_image:
        return "Не удалось сгенерировать изображение", 400

    return send_file(buffered_image, mimetype="image/png")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    port = int(os.environ["ROUTE_PORT"])
    serve(app, host="0.0.0.0", port=port)
