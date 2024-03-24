from geopy import Location as _Location
from geopy import Nominatim
from geopy.exc import GeocoderServiceError

from core.geo import GeoLocation, GeoLocator
from geo.location import GeoPyLocation


class GeoPyLocator(Nominatim, GeoLocator):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def geocode(
        self,
        query,
        **kwargs,
    ) -> GeoLocation | list[GeoLocation] | None:
        try:
            result = await super().geocode(query, **kwargs)
        except GeocoderServiceError:
            return None
        if isinstance(result, _Location):
            return GeoPyLocation(result)
        if isinstance(result, list) and all(isinstance(el, _Location) for el in result):
            return [GeoPyLocation(el) for el in result]
        return None
