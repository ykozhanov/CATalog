from telebot.states import StatesGroup, State

class CategoryDeleteStatesGroup(StatesGroup):
    ask_delete_products = State()
    confirm_delete = State()
