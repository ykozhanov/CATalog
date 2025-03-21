class KeyboardListActions:

    @property
    def action_get_all_products(self) -> str:
        return "Список товаров 🍱"

    @property
    def action_get_all_categories(self) -> str:
        return "Список категорий 🏷️"

    @property
    def action_get_product_by_name(self) -> str:
        return "Поиск по названию 🔎"

    @property
    def action_get_products_by_exp_date(self) -> str:
        return "Заканчивается срок 🔥"

    def get_reply_keyboard(self) -> list[str]:
        return [
            self.action_get_all_products,
            self.action_get_all_categories,
            self.action_get_product_by_name,
            self.action_get_products_by_exp_date,
        ]


k_list_actions = KeyboardListActions()
