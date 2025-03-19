from src.frontend.telegram.api.categories.schemas import CategoryInSchema

PREFIX_PRODUCT_ELEMENT_PAGINATOR = "product"
TEMPLATE_BUTTON_PRODUCT = "{name}: {quantity} {unit} | Годен до: {exp_date}"
ATTRS_FOR_TEMPLATE_PRODUCT = ["name", "quantity", "unit", "exp_date"]


def get_category(categories: list[CategoryInSchema], category_id: int) -> CategoryInSchema | None:
    category = None
    for c in categories:
        if c.id == category_id:
            category = c
            break
    return category
