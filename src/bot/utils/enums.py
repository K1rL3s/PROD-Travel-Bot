from core.utils.enums import StrEnum


class SlashCommand(StrEnum):
    START = "start"
    HELP = "help"
    PROFILE = "profile"
    CANCEL = "cancel"
    STOP = "stop"


class TextCommand(StrEnum):
    START = "Старт"
    HELP = "Помощь"
    PROFILE = "📖Профиль"
    TRAVELS = "✈️Путешествия"
    CANCEL = "Отмена"
    STOP = CANCEL


class BotMenu(StrEnum):
    START = "start"
    PROFILE = "profile"
    TRAVELS = "travels"
    LOCATIONS = "locations"
    NOTES = "notes"
    MEMBERS = "members"


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
