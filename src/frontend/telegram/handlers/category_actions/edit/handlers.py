from telebot.types import Message, CallbackQuery

from src.frontend.telegram.bot import telegram_bot
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.handlers.utils import (
    MainDataContextmanager,
    MainMessages,
    check_authentication_decorator,
    exc_handler_decorator,
    escape_markdown,
)
from src.frontend.telegram.handlers.utils.md_dataclasses import CategoryDataclass
from src.frontend.telegram.bot.keyboards import KeyboardYesOrNo, KeyboardActionsByElement
from src.frontend.telegram.bot.states import CategoriesStatesGroup
from src.frontend.telegram.api import CategoriesAPI
from src.frontend.telegram.api.categories.schemas import CategoryOutSchema
from .messages import CategoryUpdateActionMessages, CategoryUpdateActionTemplates, MAX_LEN_NAME
from .states import CategoryUpdateStatesGroup

__all__ = ["handle_action_update_category"]

main_m = MainMessages()
messages = CategoryUpdateActionMessages()
templates = CategoryUpdateActionTemplates()
y_or_n = KeyboardYesOrNo()


@telegram_bot.callback_query_handler(
    func=lambda m: m.data.split("#")[0] == KeyboardActionsByElement.EDIT_PREFIX,
    state=CategoriesStatesGroup.categories,
)
def handle_action_update_category(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    sm.delete_message()
    category_index = int(message.data.split("#")[1])
    with MainDataContextmanager(message) as md:
        md.category = CategoryDataclass()
        categories = md.categories
        if categories is None:
            return sm.send_message(main_m.something_went_wrong, finish_state=True)
        md.old_category = categories[category_index]
    sm.send_message(messages.input_name, state=CategoryUpdateStatesGroup.waiting_input_name)


@telegram_bot.message_handler(state=CategoryUpdateStatesGroup.waiting_input_name)
def handle_category_update_waiting_input_name(message: Message):
    sm = SendMessage(message)
    if len(message.text) > MAX_LEN_NAME:
        return sm.send_message(templates.error_max_len(MAX_LEN_NAME))
    with MainDataContextmanager(message) as md:
        md.category.name = name = message.text
    text = templates.check_md(escape_markdown(name))
    sm.send_message(
        text,
        state=CategoryUpdateStatesGroup.check_update,
        inline_keyboard=y_or_n.get_inline_keyboard(),
        parse_mode="Markdown",
    )


@telegram_bot.callback_query_handler(state=CategoryUpdateStatesGroup.check_update)
@exc_handler_decorator
@check_authentication_decorator
def handle_category_update_check_update(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == y_or_n.callback_answer_yes:
        with MainDataContextmanager(message) as md:
            category_id = md.old_category.id
            category_data = md.category
            a_token = md.user.access_jtw_token
        if a_token is None:
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
        sm.send_message(main_m.something_went_wrong, finish_state=True)


@telegram_bot.callback_query_handler(state=CategoryUpdateStatesGroup.ask_try_again)
def handle_category_update_ask_try_again(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == y_or_n.callback_answer_yes:
        with MainDataContextmanager(message) as md:
            md.category = CategoryDataclass()
        sm.send_message(messages.input_name, state=CategoryUpdateStatesGroup.waiting_input_name)
    elif message.data == y_or_n.callback_answer_no:
        sm.send_message(main_m.to_help, finish_state=True)
    else:
        sm.send_message(main_m.something_went_wrong, finish_state=True)
