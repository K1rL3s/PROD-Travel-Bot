from enum import Enum


class ValuesEnum(Enum):
    @classmethod
    def values(cls) -> list[str]:
        return [e.value for e in cls]


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return str(self.value)


class SlashCommand(StrEnum):
    START = "start"
    HELP = "help"
    PROFILE = "profile"
    CANCEL = "cancel"
    STOP = "stop"


class TextCommand(StrEnum):
    START = "Старт"
    HELP = "Помощь"
    PROFILE = "Профиль"
    CANCEL = "Отмена"
    STOP = CANCEL


class BotMenu(StrEnum):
    START = "start"
    PROFILE = "profile"
    TRAVELS = "travels"


class Action(StrEnum):
    OPEN = "open"
    CLOSE = "close"
    BACK = "back"
    FORWARD = "forware"

    GET = "get"
    ADD = "add"
    EDIT = "edit"
    DELETE = "delete"

    CONFIRM = "confirm"
    CANCEL = "cancel"


class ProfileFields(StrEnum, ValuesEnum):
    NAME = "name"
    AGE = "age"
    CITY = "city"
    DESCRIPTION = "description"
