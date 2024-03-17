from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .outer.callback_answer import CallbackAnswerMiddleware
from .outer.database import DBSessionMiddleware
from .outer.service_di import ServiceDIMiddleware
from .outer.throttling import ThrottlingMiddleware
from .outer.unknown_user import UnknownUserMiddleware
from .outer.user_context import UserContextMiddleware
from .request.retry import RetryRequestMiddleware

__all__ = ("include_global_middlewares",)


def include_global_middlewares(
    bot: "Bot",
    dp: "Dispatcher",
    session_maker: "async_sessionmaker[AsyncSession]",
) -> None:
    """Регистрация мидлварей в боте и диспетчере."""
    bot.session.middleware(RetryRequestMiddleware())

    dp.callback_query.outer_middleware(CallbackAnswerMiddleware())

    dp.update.outer_middleware(ThrottlingMiddleware())

    dp.update.outer_middleware(DBSessionMiddleware(session_maker))
    dp.update.outer_middleware(ServiceDIMiddleware())

    dp.update.outer_middleware(UserContextMiddleware())
    dp.update.outer_middleware(UnknownUserMiddleware())  # !!
