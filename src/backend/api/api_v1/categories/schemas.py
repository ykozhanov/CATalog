from pydantic import BaseModel, ConfigDict


class CategoryInSchema(BaseModel):
    name: str
    profile_id: int | None = None


class CategoryOutSchema(BaseModel):
    id: str
    name: str
    profile_id: int

    model_config = ConfigDict(
        from_attributes=True,
    )

class CategoryAllOutSchema(BaseModel):
    categories: list[CategoryOutSchema]
