from telebot.states import State, StatesGroup


class CategoryUpdateStatesGroup(StatesGroup):
    waiting_input_name = State()
    check_update = State()
    ask_try_again = State()
