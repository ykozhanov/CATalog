from telebot.states import StatesGroup, State

class ProductDeleteStatesGroup(StatesGroup):
    confirm_delete = State()
