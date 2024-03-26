import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
from redis.asyncio import Redis
from sqlalchemy.orm import close_all_sessions

from bot.handlers import include_routers
from bot.handlers.include import register_scenes
from bot.utils.enums import SlashCommand
from settings import Settings


async def on_startup(bot: Bot) -> None:
    user = await bot.me()
    logging.info(
        "Start polling for bot @%s id=%d - %r",
        user.username,
        user.id,
        user.full_name,
    )


async def on_shutdown(bot: Bot, redis: Redis) -> None:
    await redis.close()
    close_all_sessions()

    user = await bot.me()
    logging.info(
        "Stop polling for bot @%s id=%d - %r",
        user.username,
        user.id,
        user.full_name,
    )


async def set_commands(bot: Bot) -> bool:
    commands: dict[str, str] = {
        SlashCommand.START: "Старт",
        SlashCommand.HELP: "Помощь",
        SlashCommand.TRAVELS: "Твои путешествия",
        SlashCommand.PROFILE: "Твой профиль",
        SlashCommand.CANCEL: "Отмена ввода",
    }

    return await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in commands.items()
        ],
        scope=BotCommandScopeAllPrivateChats(),
    )


def create_dispatcher(
    settings: Settings,
    redis: Redis,
) -> Dispatcher:
    """Создаёт диспетчер и регистрирует все роуты."""
    storage = RedisStorage(
        redis=redis,
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )
    dp = Dispatcher(
        storage=storage,
        events_isolation=storage.create_isolation(),
        redis=redis,
        settings=settings,
        name="__main__",
    )

    include_routers(dp)
    register_scenes(dp)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    return dp


async def create_bot(bot_token: str, parse_mode: str = ParseMode.HTML) -> Bot:
    """Создаёт бота и устанавливает ему команды."""
    bot = Bot(
        token=bot_token,
        parse_mode=parse_mode,
        disable_web_page_preview=True,
    )
    await set_commands(bot)

    return bot
