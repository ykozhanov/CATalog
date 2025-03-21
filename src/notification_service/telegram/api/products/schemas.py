from datetime import date, datetime

from pydantic import BaseModel, field_validator, confloat

from .exceptions import ProductError

class ProductInSchema(BaseModel):
    id: int
    name: str
    unit: str
    quantity: confloat(ge=0)
    exp_date: date | None = None
    note: str | None = None
    category_id: int | None = None

    @field_validator("exp_date", mode="before")
    def parse_date(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, '%a, %d %b %Y %H:%M:%S GMT').date()
            except ValueError:
                raise ProductError("Дата должна быть в формате 'Thu, 20 Mar 2025 00:00:00 GMT'")
        return value


class ProductInListSchema(BaseModel):
    products: list[ProductInSchema]


class ProductOutSchema(BaseModel):
    name: str
    unit: str | None = None
    quantity: confloat(ge=0) | None = None
    exp_date: date | None = None
    note: str | None = None
    category_id: int | None = None