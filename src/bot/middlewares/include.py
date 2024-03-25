from aiogram import Bot, Dispatcher
from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from structlog.typing import FilteringBoundLogger

from settings import Settings

from .inner.processing import ProcessingMiddleware
from .outer.callback_answer import CallbackAnswerMiddleware
from .outer.core_di import ServiceDIMiddleware
from .outer.database import DBSessionMiddleware
from .outer.logging import StructLoggingMiddleware
from .outer.throttling import ThrottlingMiddleware
from .outer.unknown_user import UnknownUserMiddleware
from .outer.user_context import UserContextMiddleware
from .request.retry import RetryRequestMiddleware


def include_global_middlewares(
    bot: Bot,
    dp: Dispatcher,
    settings: Settings,
    aiohttp_session: ClientSession,
    session_maker: async_sessionmaker[AsyncSession],
    logger: FilteringBoundLogger,
) -> None:
    """Регистрация мидлварей в боте и диспетчере."""
    bot.session.middleware(RetryRequestMiddleware())

    dp.update.outer_middleware(StructLoggingMiddleware(logger))

    dp.callback_query.outer_middleware(CallbackAnswerMiddleware())

    dp.update.outer_middleware(ThrottlingMiddleware())

    dp.update.outer_middleware(DBSessionMiddleware(session_maker))
    dp.update.outer_middleware(ServiceDIMiddleware(aiohttp_session, settings))

    dp.update.outer_middleware(UserContextMiddleware())
    dp.update.outer_middleware(UnknownUserMiddleware())  # !!

    dp.message.middleware(ProcessingMiddleware())
