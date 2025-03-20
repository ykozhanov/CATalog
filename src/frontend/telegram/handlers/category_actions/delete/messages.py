from src.frontend.telegram.handlers.commands import COMMANDS


class CategoryDeleteActionMessages:
    @property
    def ask_delete_products(self) -> str:
        return "Вы хотите удалить все связанные с этой категорией товары?"


class CategoryDeleteActionTemplates:
    @staticmethod
    def confirm_all_md(name: str) -> str:
        return f"Вы действительно хотите удалить категорию *{name}* и все связанные с ней товары?"

    @staticmethod
    def confirm_only_category_md(name: str) -> str:
        return f"Вы действительно хотите удалить категорию *{name} *"\
            "и оставить сохраненными все связанные с ней товары?"

    @staticmethod
    def answer_no_md(name: str) -> str:
        return f"Отлично! Категория *{name}* не удалена!\n\nВернуться к списку действий /{COMMANDS.help[0]}"

    @staticmethod
    def success_md(name: str) -> str:
        return f"Категория *{name}* успешно удалёна!\n\nВернуться к списку действий /{COMMANDS.help[0]}"
