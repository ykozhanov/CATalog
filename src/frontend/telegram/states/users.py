from telebot.states import State, StatesGroup


class UsersStatesGroup(StatesGroup):
    login = State()
    waiting_username = State()
    waiting_password = State()
    waiting_password_repeat = State()
    waiting_email = State()
    register_check_data = State()
    ask_register_again = State()
    ask_logout = State()


class ActionsStatesGroup(StatesGroup):
    choosing_action = State()
