from aiogram.dispatcher.filters.state import State, StatesGroup


class AuthState(StatesGroup):
    social_net = State()
    service = State()
    link = State()
    plan = State()
    phone = State()
    email = State()
    comment = State()
    confirmation = State()
