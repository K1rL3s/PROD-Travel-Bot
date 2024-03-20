from aiogram import Dispatcher
from aiogram.fsm.scene import SceneRegistry

from .locations.router import locations_router
from .members.router import members_router
from .notes.router import notes_router
from .profile.router import profile_router
from .start.router import start_router
from .state_cancel.router import cancel_state_router
from .travels.router import TravelCreateScene, travels_router


def include_routers(dp: Dispatcher) -> None:
    dp.include_routers(
        start_router,
        profile_router,
        travels_router,
        locations_router,
        notes_router,
        members_router,
        cancel_state_router,
    )


def register_scenes(dp: Dispatcher) -> None:
    scene_registry = SceneRegistry(dp, register_on_add=True)
    scene_registry.add(TravelCreateScene)
