from core.utils.enums import StrEnum


class SlashCommand(StrEnum):
    START = "start"
    HELP = "help"
    PROFILE = "profile"
    TRAVELS = "travels"
    CANCEL = "cancel"
    STOP = "stop"


class TextCommand(StrEnum):
    START = "👋 Старт"
    HELP = "🤖 Помощь"
    PROFILE = "📖 Профиль"
    TRAVELS = "✈️ Путешествия"
    CANCEL = "❌ Отмена"
    STOP = CANCEL


class BotMenu(StrEnum):
    START = "start"
    PROFILE = "profile"
    TRAVELS = "travels"
    LOCATIONS = "locations"
    NOTES = "notes"
    MEMBERS = "members"
    RECOMMEND_USERS = "recommend_users"


class Action(StrEnum):
    BACK = "back"

    GET = "get"
    ADD = "add"
    EDIT = "edit"
    DELETE = "delete"

    CONFIRM = "confirm"
    CANCEL = "cancel"
