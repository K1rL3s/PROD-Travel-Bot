import datetime as dt

from aiogram import Bot, html
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.link import create_tg_link as _create_tg_link

from core.models import (
    City,
    InviteLinkExtended,
    LocationExtended,
    TravelExtended,
    UserExtended,
    Weather,
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
{html.bold("Время прибытия:")} {format_datetime(location.start_at)} ({location.city.timezone})
""".strip()


def format_member(user: UserExtended) -> str:
    return (
        f"Участник {f'@{user.tg_username}' if user.tg_username else create_tg_link(user.name, 'user', id=user.id)}\n"
        + format_user(user)
    )


async def format_invite_link(link: InviteLinkExtended, bot: Bot) -> str:
    return f"""
🎫 Привет! Приглашаю тебя со мной в путешествие «{link.travel.title}».
👇 Переходи по этой пригласительной ссылке и отправляйся в наше приключение!
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


def format_weather(city: City, current: Weather | None, future: Weather | None) -> str:
    return f"""
Погода в "{html.bold(city.title)}" сегодня:
{format_single_weather(current) if current else NO_DATA}

Погода в "{html.bold(city.title)}" через 5 дней:
{format_single_weather(future) if future else NO_DATA}
""".strip()


def format_single_weather(weather: Weather) -> str:
    return f"""
{html.bold(weather.description.capitalize())}
Сейчас {html.bold(f"{weather.temp}°C")}, ощущается как {html.bold(f"{weather.feels_like}°C")}
Перепады от {html.bold(f'{weather.temp_min}°C')} до {html.bold(f'{weather.temp_max}°C')}
Скорость ветра {html.bold(f'{weather.wind_speed}м/с')}
Давление {html.bold(f'{round(weather.pressure / 1.333)} мм рт. ст.')}
Влажность {html.bold(f'{weather.humidity}%')}
Видимость {html.bold(f'{weather.visibility}м.')}
""".strip()


def format_datetime(datetime: dt.datetime) -> str:
    return datetime.strftime("%d.%m.%Y %H:%M:%S")
