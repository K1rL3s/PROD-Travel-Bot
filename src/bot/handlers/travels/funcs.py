from aiogram import html

from core.models import TravelExtended


def format_travel(travel: TravelExtended) -> str:
    return f"""
{html.bold("Название")}: {travel.title}
{html.bold("Описание")}:\n{travel.description}
    """.strip()
