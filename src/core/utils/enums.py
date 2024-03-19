from enum import Enum


class ValuesEnum(Enum):
    @classmethod
    def values(cls) -> list[str]:
        return [e.value for e in cls]


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return str(self.value)


class ProfileField(StrEnum, ValuesEnum):
    NAME = "name"
    AGE = "age"
    CITY = "city"
    COUNTRY = "country"
    DESCRIPTION = "description"


class TravelField(StrEnum, ValuesEnum):
    TITLE = "title"
    DESCRIPTION = "description"


class LocationField(StrEnum, ValuesEnum):
    TITLE = "title"
    COUNTRY = "country"
    CITY = "city"
    ADDRESS = "address"
    START_AT = "start_at"
    END_AT = "end_at"


class NoteField(StrEnum, ValuesEnum):
    TITLE = "title"
