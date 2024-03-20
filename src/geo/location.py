from geopy import Location as _Location

from core.geo import GeoLocation


class GeoPyLocation(_Location, GeoLocation):
    pass
