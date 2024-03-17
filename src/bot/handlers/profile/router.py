from aiogram import F, Router

from bot.callbacks.profile import ProfileData
from bot.utils.enums import Action

from .check import router as check_router
from .edit import router as edit_router
from .fill import ProfileFillScene

router = Router(name=__name__)
router.callback_query.register(
    ProfileFillScene.as_handler(),
    ProfileData.filter(F.action == Action.ADD),
)
router.include_routers(check_router, edit_router)
