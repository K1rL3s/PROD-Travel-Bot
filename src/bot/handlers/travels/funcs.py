from aiogram import html

from core.models import Travel


def format_travel(travel: Travel) -> str:
    return f"""
{html.bold("Название")}: {travel.title}
{html.bold("Описание")}:\n{travel.description}
    """.strip()
