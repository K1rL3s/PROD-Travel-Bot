from aiogram.fsm.state import State, StatesGroup


class ProfileCreating(StatesGroup):
    name = State()
    age = State()
    city = State()
    country = State()
    descirption = State()


class ProfileState(StatesGroup):
    editing = State()


class TravelState(StatesGroup):
    editing = State()


class LocationState(StatesGroup):
    editing = State()


class NoteCreating(StatesGroup):
    title = State()
    status = State()
    file = State()
