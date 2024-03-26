from geopy import Location as _Location

from core.geo import GeoLocation


class GeoPyLocation(_Location, GeoLocation):
    def __init__(self, location: _Location) -> None:
        super().__init__(location.address, location.point, location.raw)

    @property
    def local_title(self) -> str | None:
        address = self.raw.get("address", {})
        return (
            address.get(self.raw.get("addresstype"))
            or address.get("city")
            or address.get("municipality")
            or address.get("town")
            or address.get("village")
        )

    @property
    def country_title(self) -> str | None:
        return self.raw.get("address", {}).get("country")

    @property
    def country_code(self) -> str | None:
        address = self.raw.get("address", {})
        extratags = address.get("extratags", {})
        return (
            address.get("country_code").upper()
            or extratags.get("ISO3166-1:alpha2").upper()
            or extratags.get("country_code_iso3166_1_alpha_2").upper()
        )
