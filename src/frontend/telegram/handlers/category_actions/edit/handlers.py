from telebot.types import Message, CallbackQuery

from src.frontend.telegram.settings import BOT
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.handlers.utils import (
    MainDataContextmanager,
    MainMessages,
    check_authentication_decorator,
    exc_handler_decorator,
)
from src.frontend.telegram.handlers.utils.md_dataclasses import CategoryDataclass
from src.frontend.telegram.bot.keyboards import KeyboardYesOrNo, KeyboardActionsByElement
from src.frontend.telegram.bot.states import CategoriesStatesGroup
from src.frontend.telegram.api import CategoriesAPI
from src.frontend.telegram.api.categories.schemas import CategoryOutSchema
from .messages import CategoryUpdateActionMessages, CategoryUpdateActionTemplates
from .states import CategoryUpdateStatesGroup

main_m = MainMessages()
messages = CategoryUpdateActionMessages()
templates = CategoryUpdateActionTemplates()
y_or_n = KeyboardYesOrNo()


@BOT.callback_query_handler(
    func=lambda m: m.data.split("#")[0] == KeyboardActionsByElement.EDIT_PREFIX,
    state=CategoriesStatesGroup.categories,
)
def handle_action_update_product(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    sm.delete_message()
    category_index = int(message.data.split("#")[1])
    with MainDataContextmanager(message) as md:
        md.product = CategoryDataclass()
        if categories := md.categories is None:
            return sm.send_message(main_m.something_went_wrong, finish_state=True)
        md.old_category = categories[category_index]
    sm.send_message(
        text=messages.input_name,
        state=CategoryUpdateStatesGroup.waiting_input_name,
    )


@BOT.message_handler(state=CategoryUpdateStatesGroup.waiting_input_name)
def handle_category_update_waiting_input_name(message: Message):
    sm = SendMessage(message)
    with MainDataContextmanager(message) as md:
        md.product.name = name = message.text
    sm.send_message(
        templates.check_md(name),
        state=CategoryUpdateStatesGroup.check_update,
        inline_keyboard=y_or_n.get_inline_keyboard(),
    )


@exc_handler_decorator
@check_authentication_decorator
@BOT.callback_query_handler(state=CategoryUpdateStatesGroup.check_update)
def handle_category_update_check_update(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == y_or_n.callback_answer_yes:
        with MainDataContextmanager(message) as md:
            category_id = md.old_category.id
            category_data = md.category
            if a_token := md.user.access_jtw_token is None:
                return sm.send_message(main_m.something_went_wrong, finish_state=True)
        c_api = CategoriesAPI(a_token)
        category = CategoryOutSchema(**category_data.dict())
        c_api.put(category_id, category)
        with MainDataContextmanager(message) as md:
            md.category = None
            md.old_category = None
        sm.send_message(messages.success, finish_state=True)
    elif message.data == y_or_n.callback_answer_no:
        sm.send_message(
            text=messages.try_again,
            state=CategoryUpdateStatesGroup.ask_try_again,
            inline_keyboard=y_or_n.get_inline_keyboard(),
        )
    else:
        sm.send_message(text=main_m.something_went_wrong, finish_state=True)


@BOT.callback_query_handler(state=CategoryUpdateStatesGroup.ask_try_again)
def handle_category_update_ask_try_again(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == y_or_n.callback_answer_yes:
        with MainDataContextmanager(message) as md:
            md.product = CategoryDataclass()
        sm.send_message(
            text=messages.input_name,
            state=CategoryUpdateStatesGroup.waiting_input_name,
        )
    elif message.data == y_or_n.callback_answer_no:
        sm.send_message(main_m.to_help, finish_state=True)
    else:
        sm.send_message(text=main_m.something_went_wrong, finish_state=True)
