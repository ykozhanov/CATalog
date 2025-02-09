from pydantic import BaseModel


class UserInSchema(BaseModel):
    access_token: str
    refresh_token: str
