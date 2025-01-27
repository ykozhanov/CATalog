from telebot.states import State, StatesGroup


class CategoryCreateStatesGroup(StatesGroup):
    ask_add_new = State()
    waiting_input_name = State()
    check_new = State()
