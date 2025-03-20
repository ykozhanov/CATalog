from datetime import datetime
from telebot.types import Message, CallbackQuery

from src.frontend.telegram.handlers.actions.get_all_categories.utils import (
    get_all_categories,
    PREFIX_CATEGORY_ELEMENT_PAGINATOR,
)


def get_inline_categories(message: Message | CallbackQuery) -> list[tuple[str, str]]:
    categories = get_all_categories(message)
    return [(c.name, f"{PREFIX_CATEGORY_ELEMENT_PAGINATOR}#{c.id}#{c.name}") for c in categories]


def year_str_to_int(year: str | int) -> int:
    year_str = str(year)
    try:
        return datetime.strptime(year_str, "%Y").year
    except ValueError:
        return datetime.strptime(year_str, "%y").year


def day_str_to_int(day: str | int) -> int:
    day_int = int(day)
    if day_int < 1 or day_int > 31:
        raise ValueError
    return day_int


def month_str_to_int(month: str | int) -> int:
    month_int = int(month)
    if month_int < 1 or month_int > 12:
        raise ValueError
    return month_int
