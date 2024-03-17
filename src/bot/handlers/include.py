from aiogram import Dispatcher
from aiogram.fsm.scene import SceneRegistry

from .profile.router import ProfileCreateScene, profile_router
from .start.router import start_router
from .state_cancel.router import cancel_state_router
from .travels.router import TravelCreateScene, travels_router


def include_routers(dp: Dispatcher) -> None:
    dp.include_routers(
        start_router,
        cancel_state_router,
        profile_router,
        travels_router,
    )


def register_scenes(dp: Dispatcher) -> None:
    scene_registry = SceneRegistry(dp)
    scene_registry.add(
        ProfileCreateScene,
        TravelCreateScene,
    )
