from aiogram import html

from core.models import User


def format_user_profile(user: User) -> str:
    return f"""
{html.bold("Имя")}: {user.name}
{html.bold("Возраст")}: {user.age}
{html.bold("Город")}: {user.city}
{html.bold("Страна")}: {user.country}
{html.bold("Описание")}:\n{user.description}
    """.strip()
