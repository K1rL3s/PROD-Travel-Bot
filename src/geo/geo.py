from geopy import Nominatim

from core.geo import GeoLocator


class GeoPyLocator(Nominatim, GeoLocator):
    pass
