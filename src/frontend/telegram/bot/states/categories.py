from telebot.states import State, StatesGroup


class CategoriesStatesGroup(StatesGroup):
    ask_add_new_category = State()
    categories = State()
    # category = State()
