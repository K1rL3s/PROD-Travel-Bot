from aiogram import Router

from bot.callbacks.location import AddLocationData
from bot.filters.travel import TravelCallbackAccess

from .check import router as check_router
from .create import LocationCreateScene
from .delete import router as delete_router
from .edit import router as edit_router
from .no_access import router as no_access_router

locations_router = Router(name=__name__)

locations_router.callback_query.register(
    LocationCreateScene.as_handler(),
    AddLocationData.filter(),
    TravelCallbackAccess(),
)

locations_router.include_routers(
    check_router,
    edit_router,
    delete_router,
    no_access_router,
)
