from aiogram import Router

from bot.callbacks import AddTravelData

from .check import router as check_router
from .create import TravelCreateScene
from .delete import router as delete_router
from .edit import router as edit_router
from .leave import router as leave_router
from .no_access import router as no_access_router
from .routing import router as routing_router

travels_router = Router(name=__name__)

travels_router.callback_query.register(
    TravelCreateScene.as_handler(),
    AddTravelData.filter(),
)
travels_router.include_routers(
    check_router,
    edit_router,
    delete_router,
    routing_router,
    leave_router,
    no_access_router,
)
