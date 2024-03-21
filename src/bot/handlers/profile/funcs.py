from aiogram import html

from core.models import UserExtended


def format_user_profile(user: UserExtended) -> str:
    return f"""
{html.bold("Имя")}: {user.name}
{html.bold("Возраст")}: {user.age}
{html.bold("Страна")}: {user.country}
{html.bold("Город")}: {user.city}
{html.bold("Описание")}:\n{user.description}
    """.strip()
