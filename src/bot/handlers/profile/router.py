from aiogram import Router

from .check import router as check_router
from .create import router as create_router
from .edit import router as edit_router

profile_router = Router(name=__name__)

profile_router.include_routers(
    create_router,
    check_router,
    edit_router,
)
