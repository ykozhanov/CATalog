from pydantic import BaseModel, Field


class UserInSchema(BaseModel):
    access_jtw_token: str = Field(..., alias="access_token")
    refresh_jtw_token: str = Field(..., alias="refresh_token")
