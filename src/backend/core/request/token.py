from datetime import datetime
from typing import Literal

from pydantic import BaseModel, field_validator

TOKEN_STARTSWITH_BEARER = "Bearer "
TOKEN_STARTSWITH_BASIC = "Basic "

Type_JWT = Literal["access", "refresh"]
TYPE_ACCESS_JWT: Type_JWT = "access"
TYPE_REFRESH_JWT: Type_JWT = "refresh"


class JWTPayloadSchema(BaseModel):
    sub: str
    iat: datetime
    exp: datetime
    jti: str
    type: Type_JWT

    @classmethod
    @field_validator("sub", mode="before")
    def parse_sub(cls, value):
        if isinstance(value, int):
            try:
                return str(value)
            except TypeError:
                raise TypeError("Атрибут 'sub' должен быть str или int")
        return value
