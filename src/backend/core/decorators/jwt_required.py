from typing import Callable
from functools import wraps

from flask import request

from src.backend.settings import SUB_PAYLOAD_JWT, USER_MODEL, AUTH_HEADER
from ..mixins import JWTMixin
from ..exceptions import AuthenticationError
from ..settings.database import crud


def jwt_required(func: Callable) -> Callable:

    @wraps(func)
    def wrapped(self: JWTMixin, *args, **kwargs) -> Callable:
        auth_header = request.headers.get(AUTH_HEADER)
        if not auth_header or not auth_header.startswith("Bearer "):
            raise AuthenticationError("Отсутствует JWT токен или неверный тип токена")
        payload = self._decode_jwt(token=auth_header.split()[1], exc=AuthenticationError)
        user_id_str = payload.get(SUB_PAYLOAD_JWT)
        if not isinstance(user_id_str, str):
            raise AuthenticationError("Ошибка токена")
        user_id = int(user_id_str)
        current_user = crud.read(USER_MODEL, user_id)
        if not current_user:
            raise AuthenticationError("Ошибка аутентификации")
        return func(self, current_user, *args, **kwargs)

    return wrapped
