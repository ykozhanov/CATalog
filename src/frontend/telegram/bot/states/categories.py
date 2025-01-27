from telebot.states import State, StatesGroup


class CategoriesStatesGroup(StatesGroup):
    categories = State()
