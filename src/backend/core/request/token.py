from datetime import datetime
from typing import Literal

from pydantic import BaseModel

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
