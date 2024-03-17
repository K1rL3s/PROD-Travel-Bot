from aiogram import F, Router

from bot.callbacks.profile import ProfileData
from bot.utils.enums import Action

from .check import router as check_router
from .create import ProfileCreateScene
from .edit import router as edit_router

profile_router = Router(name=__name__)

profile_router.callback_query.register(
    ProfileCreateScene.as_handler(),
    ProfileData.filter(F.action == Action.ADD),
)
profile_router.include_routers(check_router, edit_router)
