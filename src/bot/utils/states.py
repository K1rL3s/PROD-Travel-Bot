from aiogram.fsm.state import State, StatesGroup


class ProfileState(StatesGroup):
    editing = State()


class TravelState(StatesGroup):
    editing = State()


class LocationState(StatesGroup):
    editing = State()
