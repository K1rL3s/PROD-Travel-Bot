from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link

from core.models import InviteLinkExtended, User


def format_member(member: User) -> str:
    return f"""
{member}
""".strip()


async def format_invite_link(link: InviteLinkExtended, bot: Bot) -> str:
    return f"""
{link}
{await create_start_link(bot, str(link.id), encode=True)}
""".strip()
