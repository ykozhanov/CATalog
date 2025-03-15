from pydantic import BaseModel


class CategoryInSchema(BaseModel):
    id: int
    name: str


class CategoryInListSchema(BaseModel):
    categories: list[CategoryInSchema]


class CategoryOutSchema(BaseModel):
    name: str
