import os
from functools import lru_cache

from pydantic import BaseModel


class DBSettings(BaseModel):
    """Настройки подключения к базе данных."""

    host: str
    host_port: int
    db: str
    user: str
    password: str


class RedisSettings(BaseModel):
    """Настройки редиса."""

    host: str
    host_port: int
    password: str


class BotSettings(BaseModel):
    """Настройки телеграм-бота."""

    token: str


class APISettings(BaseModel):
    """Ключ к апишками."""

    open_weather_key: str


class Settings(BaseModel):
    """Сборник настроек :)."""

    db: DBSettings
    redis: RedisSettings
    bot: BotSettings
    api: APISettings


@lru_cache
def get_settings() -> Settings:
    """
    Создание настроек из переменных среды.

    :return: Настройки.
    """
    db = DBSettings(
        host=os.environ["POSTGRES_HOST"],
        host_port=int(os.environ["POSTGRES_HOST_PORT"]),
        db=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )
    redis = RedisSettings(
        host=os.environ["REDIS_HOST"],
        host_port=int(os.environ["REDIS_HOST_PORT"]),
        password=os.environ["REDIS_PASSWORD"],
    )
    bot = BotSettings(
        token=os.environ["BOT_TOKEN"],
    )
    api = APISettings(open_weather_key=os.environ["OPEN_WEATHER_KEY"])

    return Settings(db=db, redis=redis, bot=bot, api=api)
