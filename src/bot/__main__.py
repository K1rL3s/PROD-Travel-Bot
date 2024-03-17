import asyncio
import contextlib

from bot.factory import create_bot, create_dispatcher
from bot.logger import setup_logs
from bot.middlewares import include_global_middlewares
from database.session import database_init, redis_init
from settings import get_settings


async def main() -> None:
    setup_logs()

    settings = get_settings()
    redis = await redis_init(settings.redis)
    session_maker = await database_init(settings.db)

    bot = await create_bot(settings.bot.token)
    dp = create_dispatcher(settings, redis)

    include_global_middlewares(bot, dp, session_maker)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
