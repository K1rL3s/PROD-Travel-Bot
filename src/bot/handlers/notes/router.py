from aiogram import Router

from .check import router as check_router
from .create import router as create_router
from .delete import router as delete_router
from .edit import router as edit_router
from .no_access import router as no_access_router

notes_router = Router(name=__name__)
notes_router.include_routers(
    check_router,
    create_router,
    delete_router,
    edit_router,
    no_access_router,
)
