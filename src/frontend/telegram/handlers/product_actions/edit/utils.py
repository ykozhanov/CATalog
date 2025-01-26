from telebot.types import Message, CallbackQuery

from src.frontend.telegram.handlers.actions.get_all_categories.utils import (
    PREFIX_CATEGORY_ELEMENT_PAGINATOR,
    get_all_categories,
)


def get_inline_categories(message: Message | CallbackQuery) -> list[tuple[str, str]]:
    categories = get_all_categories(message)
    return [(c.name, f"{PREFIX_CATEGORY_ELEMENT_PAGINATOR}#{c.id}#{c.name}") for c in categories]
