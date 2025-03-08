from pydantic import BaseModel, ConfigDict


class CategoryInSchema(BaseModel):
    name: str


class CategoryOutSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True,
    )

class CategoryListOutSchema(BaseModel):
    categories: list[CategoryOutSchema]
