from telebot.states import State, StatesGroup


class ProductsStatesGroup(StatesGroup):
    ask_add_new_product = State()
    products = State()
    product = State()
    waiting_name_product = State()
