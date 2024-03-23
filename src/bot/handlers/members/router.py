from aiogram import Router

from .check import router as check_router
from .delete import router as delete_router
from .invite import router as invite_router
from .recommend import router as recommend_router

members_router = Router(name=__name__)
members_router.include_routers(
    check_router,
    delete_router,
    invite_router,
    recommend_router,
)
