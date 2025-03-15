from telebot.types import Message, CallbackQuery

from src.frontend.telegram.api.categories.categories_api import CategoriesAPI
from src.frontend.telegram.api.categories.schemas import CategoryInSchema
from src.frontend.telegram.handlers.utils import MainDataContextmanager

PREFIX_CATEGORY_ELEMENT_PAGINATOR = "category"
TEMPLATE_BUTTON_CATEGORY = "{name}"
ATTRS_FOR_TEMPLATE_CATEGORY = ["name"]


def get_all_categories(message: Message | CallbackQuery) -> list[CategoryInSchema] | None:
    with MainDataContextmanager(message) as md:
        a_token = md.user.access_jtw_token
    if a_token:
        c_api = CategoriesAPI(a_token)
        with MainDataContextmanager(message) as md:
            md.categories = c_api.get_all()
            return md.categories
    else:
        return None
