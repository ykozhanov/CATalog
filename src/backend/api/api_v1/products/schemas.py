from datetime import date, datetime

from pydantic import BaseModel, field_validator, ConfigDict, confloat


class ProductInSchema(BaseModel):
    name: str
    unit: str | None = None
    quantity: confloat(ge=0) | None = None
    exp_date: date = None
    note: str | None = None
    category_id: int | None = None

    # @classmethod
    # @field_validator("exp_date", mode="before")
    # def parse_date(cls, value):
    #     if isinstance(value, str):
    #         try:
    #             return datetime.strptime(value, '%Y-%m-%d').date()
    #         except ValueError:
    #             raise ValueError("Дата должна быть в формате YYYY-MM-DD")
    #     return value


class ProductOutSchema(BaseModel):
    id: int
    name: str
    unit: str
    quantity: confloat(ge=0)
    exp_date: date | None = None
    note: str | None = None
    category_id: int | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )


class ProductListOutSchema(BaseModel):
    products: list[ProductOutSchema]
