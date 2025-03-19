from datetime import date, datetime

from pydantic import BaseModel, field_validator, ConfigDict, confloat


class ProductInSchema(BaseModel):
    name: str
    unit: str | None = None
    quantity: confloat(ge=0) | None = None
    exp_date: date | None = None
    note: str | None = None
    category_id: int | None = None


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
