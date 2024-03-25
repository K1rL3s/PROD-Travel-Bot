from aiogram.fsm.state import State, StatesGroup


class ProfileCreating(StatesGroup):
    name = State()
    age = State()
    city = State()
    country = State()
    descirption = State()


class NoteCreating(StatesGroup):
    title = State()
    status = State()
    file = State()


class LocationCreating(StatesGroup):
    title = State()
    city = State()
    country = State()
    address = State()
    start_at = State()
    end_at = State()


class ProfileState(StatesGroup):
    editing = State()
    editing_city = State()
    editing_country = State()


class TravelState(StatesGroup):
    editing = State()


class LocationState(StatesGroup):
    editing = State()
    editing_city = State()
    editing_country = State()
    editing_start_at = State()
