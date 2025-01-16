from datetime import date, datetime

from pydantic import BaseModel, field_validator


class ProductInSchema(BaseModel):
    id: int
    name: str
    unit: str
    quantity: int
    exp_date: date | None = None
    note: str | None = None

    # @classmethod
    # @field_validator("exp_date", mode="before")
    # def parse_date(cls, value):
    #     if isinstance(value, str):
    #         try:
    #             return datetime.strptime(value, '%Y-%m-%d').date()
    #         except ValueError:
    #             raise ValueError("Дата должна быть в формате YYYY-MM-DD")
    #     return value


class ProductInListSchema(BaseModel):
    products: list[ProductInSchema]


class ProductOutSchema(BaseModel):
    name: str
    unit: str | None = None
    quantity: int | None = None
    exp_date: date | None = None
    note: str | None = None
