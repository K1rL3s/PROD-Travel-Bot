from aiogram import Bot, html
from aiogram.utils.deep_linking import create_start_link

from core.models import (
    InviteLinkExtended,
    LocationExtended,
    TravelExtended,
    User,
    UserExtended,
)


def format_travel(travel: TravelExtended) -> str:
    return f"""
{html.bold("Название")}: {travel.title}
{html.bold("Описание")}:\n{travel.description}
    """.strip()


def format_location(location: LocationExtended) -> str:
    return f"""
{location}
""".strip()


def format_member(member: User) -> str:
    return f"""
{member}
""".strip()


async def format_invite_link(link: InviteLinkExtended, bot: Bot) -> str:
    return f"""
{link}
{await create_start_link(bot, str(link.id), encode=True)}
""".strip()


def format_user_profile(user: UserExtended) -> str:
    return f"""
{html.bold("Имя")}: {user.name}
{html.bold("Возраст")}: {user.age}
{html.bold("Страна")}: {user.country}
{html.bold("Город")}: {user.city}
{html.bold("Описание")}:\n{user.description}
    """.strip()
