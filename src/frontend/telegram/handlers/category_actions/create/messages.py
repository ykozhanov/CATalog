class CategoryCreateActionMessages:
    @property
    def input_name(self) -> str:
        return "Введите название новой категории:"


    @property
    def try_again(self) -> str:
        return "Попробовать снова?"

    @property
    def success(self) -> str:
        return "Новый товар успешно создан!\nВернуться к списку действий /help"


class CategoryCreateActionTemplates:
    @staticmethod
    def check_md(
            name: str,
    ) -> str:
        return f"""Новый категория:
            **Имя**: {name}.
        
        Всё верно?
        """
