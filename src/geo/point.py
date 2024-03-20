from geopy import Point as _Point

from core.geo import GeoPoint


class GeoPyPoint(_Point, GeoPoint):
    pass
