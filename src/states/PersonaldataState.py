from aiogram.dispatcher.filters.state import StatesGroup, State


class PersonalData(StatesGroup):
    gender = State()
    interests = State()
    age = State()
