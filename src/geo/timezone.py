from tzfpy import get_tz

from core.geo import Timezoner


class TzfTimezoner(Timezoner):
    async def get_timezone(self, latitude: float, longitude: float) -> str:
        return get_tz(lat=latitude, lng=longitude)
