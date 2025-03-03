from aiogram.dispatcher.filters.state import StatesGroup, State


class AuthState(StatesGroup):
    social_net = State()
    service = State()
    link = State()
    price = State()
    phone = State()
    payment = State()




