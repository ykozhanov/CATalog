from typing import Any
from datetime import date
from dataclasses import dataclass, asdict

from src.frontend.telegram.core.database.models import User
from src.frontend.telegram.api.products.schemas import ProductInSchema
from src.frontend.telegram.api.categories.schemas import CategoryInSchema


@dataclass
class ProductDataclass:
    name: str | None = None
    unit: str | None = None
    quantity: float | None = None
    exp_date: date | None = None
    exp_date_year: int | None = None
    exp_date_month: int | None = None
    exp_date_day: int | None = None
    note: str | None = None
    category_id: int | None = None
    category_name: str | None = None

    def dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CategoryDataclass:
    name: str | None = None
    delete_all_products: bool | None = None

    def dict(self) -> dict[str, Any]:
        return asdict(self)


@classmethod
class LoginDataclass:
    register: bool | None = None
    username: str | None = None
    password: str | None = None
    email: str | None = None

    def dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class MainDataclass:
    user: User | None = None
    login: LoginDataclass | None = None
    product: ProductDataclass | None = None
    old_product: ProductInSchema | None = None
    category: CategoryDataclass | None = None
    old_category: CategoryInSchema | None = None
    products: list[ProductInSchema] | None = None
    categories: list[CategoryInSchema] | None = None

    def dict(self) -> dict[str, Any]:
        return asdict(self)
