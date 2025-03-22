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
    name: str

    def dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass
class Product:
    name: str
    unit: str | None = None
    quantity: float | None = None
    exp_date: date | None = None
    note: str | None = None
    category_id: int | None = None

    def dict(self) -> dict[str, Any]:
        return asdict(self)


test_user = Credential(username="test", password="test", email="test@test.ru")
test_category = Category(name="test_category")
test_update_category = Category(name="test_update_category")
