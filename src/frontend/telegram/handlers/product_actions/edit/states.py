from telebot.states import State, StatesGroup


class ProductUpdateStatesGroup(StatesGroup):
    ask_input_name = State()
    waiting_input_name = State()
    ask_input_unit = State()
    waiting_input_unit = State()
    ask_input_quantity = State()
    waiting_input_quantity = State()
    ask_input_exp_date = State()
    waiting_input_day = State()
    waiting_input_month = State()
    waiting_input_year = State()
    ask_input_note = State()
    waiting_input_note = State()
    ask_choice_category = State()
    waiting_choice_category = State()
    check_update_product = State()
    ask_try_again = State()
