from src.frontend.telegram.handlers.commands import COMMANDS


class ProductDeleteActionTemplates:
    @staticmethod
    def confirm_md(name: str) -> str:
        return f"Вы действительно хотите удалить товар **{name}**?"

    @staticmethod
    def answer_no_md(name: str) -> str:
        return f"Отлично! Товар **{name}** не удалён!\n\nВернуться к списку действий /{COMMANDS.help[0]}"

    @staticmethod
    def success_md(name: str) -> str:
        return f"Товар **{name}** успешно удалён!\n\nВернуться к списку действий /{COMMANDS.help[0]}"
