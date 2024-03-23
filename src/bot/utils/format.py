from aiogram import Bot, html
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.link import create_tg_link as _create_tg_link

from core.models import (
    InviteLinkExtended,
    LocationExtended,
    TravelExtended,
    UserExtended,
)

NO_DATA = "-"


def create_tg_link(text: str, link: str, **kwargs) -> str:
    return html.link(text, _create_tg_link(link, **kwargs))


def format_travel(travel: TravelExtended) -> str:
    return f"""
{html.bold("Название")}: {travel.title}
{html.bold("Описание")}:\n{travel.description}
""".strip()


def format_location(location: LocationExtended) -> str:
    return f"""
Локация путешествия "{location.travel.title}"
{html.bold("Название:")}  {location.title}
{html.bold("Местоположение:")} {location.country.title}, {location.city.title}, {location.address}
{html.bold("Время прибытия:")} {location.start_at}
""".strip()


def format_member(user: UserExtended) -> str:
    return (
        f"Участник {f'@{user.tg_username}' if user.tg_username else create_tg_link(user.name, 'user', id=user.id)}\n"
        + format_user(user)
    )


async def format_invite_link(link: InviteLinkExtended, bot: Bot) -> str:
    return f"""
🎫 Привет! Приглашаю тебя со мной в путешествие «{link.travel.title}».
👇 Переходи по этой пригласительной ссылке и отправимся в приключение
{await create_start_link(bot, str(link.id), encode=True)}
""".strip()


def format_user(user: UserExtended) -> str:
    return f"""
{html.bold("Имя")}: {user.name}
{html.bold("Возраст")}: {user.age}
{html.bold("Страна")}: {user.country.title}
{html.bold("Город")}: {user.city.title}
{html.bold("Описание")}:\n{user.description or NO_DATA}
""".strip()
