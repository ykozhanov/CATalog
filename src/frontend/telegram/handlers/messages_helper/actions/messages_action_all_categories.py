from dataclasses import dataclass


@dataclass
class MessagesActionGetAllCategories:

    @property
    def message_categories_empty(self) -> str:
        return "У вас пока не ни одного товара, добавить?"

    @staticmethod
    def template_message_get_list_all_categories_md(name: str) -> str:
        return f"""О категории:
            **Имя**: {name}.
        """


MESSAGES_ACTION_GET_ALL_CATEGORIES = MessagesActionGetAllCategories()
