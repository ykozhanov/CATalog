from datetime import datetime
from telebot.types import Message, CallbackQuery

from src.frontend.telegram.handlers.actions.get_all_categories.utils import (
    get_all_categories,
    PREFIX_CATEGORY_ELEMENT_PAGINATOR,
)

def get_inline_categories(message: Message | CallbackQuery) -> list[tuple[str, str]]:
    categories = get_all_categories(message)
    return [(c.name, f"{PREFIX_CATEGORY_ELEMENT_PAGINATOR}#{c.id}#{c.name}") for c in categories]


def check_and_get_year(message: str) -> int | None:
    try:
        return datetime.strptime(message, "%Y").year
    except ValueError:
        try:
            return datetime.strptime(message, "%y").year
        except ValueError:
            return None
