from aiogram import Dispatcher
from aiogram.fsm.scene import SceneRegistry

from bot.handlers.profile.router import ProfileFillScene
from bot.handlers.profile.router import router as profile_router

from .start.router import router as start_router
from .state_cancel.router import router as cancel_state_router


def include_routers(dp: Dispatcher) -> None:
    dp.include_routers(
        start_router,
        cancel_state_router,
        profile_router,
    )


def register_scenes(dp: Dispatcher) -> None:
    scene_registry = SceneRegistry(dp)
    scene_registry.add(ProfileFillScene)
