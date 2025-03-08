class CategoryListActionTemplates:
    @staticmethod
    def list_md(name: str) -> str:
        return f"Список товаров из категории *{name}*"

    @staticmethod
    def empty_md(name: str) -> str:
        return f"У вас пока нет ни одного товара в категории *{name}*, добавить?"
