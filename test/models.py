import json
from dataclasses import dataclass, asdict
from datetime import date
from typing import Any


@dataclass
class Credential:
    username: str
    password: str
    email: str | None = None


@dataclass
class JWTTokens:
    access_token: str | None
    refresh_token: str | None


@dataclass
class Category:
    id: int
    name: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class Product:
    id: int
    name: str
    unit: str | None = None
    quantity: float | None = None
    exp_date: date | None = None
    note: str | None = None
    category_id: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


# Экземпляры

test_user = Credential(username="test", password="test", email="test@test.ru")

test_category = Category(id=1, name="test_category")
test_update_category = Category(id=1, name="test_update_category")

test_product = Product(
    id=1,
    name="test_product",
    unit="ед.",
    quantity=5,
    exp_date=date(year=2025, month=1, day=1),
    note="заметка",
    category_id=test_category.id,
)

test_update_product = Product(
    id=1,
    name="test_update_product",
    unit="ед.",
    quantity=5,
    exp_date=date(year=2025, month=1, day=1),
    note="заметка",
    category_id=test_category.id,
)
