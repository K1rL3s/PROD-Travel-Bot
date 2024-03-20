from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Update
from aiogram.types import User as TGUser

from bot.middlewares.base import BaseInfoMiddleware
from core.models import User
from core.services.user import UserService


class UserContextMiddleware(BaseInfoMiddleware):
    """Мидлварь, который добавляет информацию о юзере из бд в контекст."""

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        user_service: UserService = data["user_service"]
        event_from_user: TGUser | None = data.get("event_from_user")

        if event_from_user:
            user = await user_service.get(event_from_user.id)
            if user:
                data["user"] = User.model_validate(user)

        return await handler(event, data)
