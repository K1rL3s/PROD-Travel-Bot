from aiogram import Router

from .check import router as check_router
from .create import router as create_router
from .delete import router as delete_router
from .edit import router as edit_router
from .no_access import router as no_access_router
from .weather import router as weather_router

locations_router = Router(name=__name__)

locations_router.include_routers(
    check_router,
    create_router,
    edit_router,
    delete_router,
    weather_router,
    no_access_router,
)
