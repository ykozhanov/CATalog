from typing import Callable, TypeVar
from functools import wraps

from flask import request, jsonify, Response
from pydantic import ValidationError

from src.backend.core.mixins import JWTMixin
from src.backend.core.exceptions import AuthenticationError
from src.backend.core.exceptions.messages import MESSAGE_TOKEN_INVALID_401
# from src.backend.core.settings_app import AUTH_HEADER
from src.backend.core.response import ErrorMessageSchema
from src.backend.core.request import Type_JWT, TOKEN_STARTSWITH_BEARER, JWTPayloadSchema

from .base64_login import AUTH_HEADER

R = TypeVar("R")


def get_jwt_token_decorator(type_token: Type_JWT) -> Callable[[Callable[..., R]], Callable[..., tuple[Response, int] | R]]:
    """Декоратор для проверки JWT токена.

      Этот декоратор извлекает заголовок авторизации из запроса, проверяет его на наличие
      токена в формате Bearer и декодирует его. Если токен валиден и соответствует ожидаемому
      типу, он передается в декорируемую функцию первым (позиционным) аргументом как строка.

      Args:
          type_token (Type_JWT): Ожидаемый тип токена (например, access или refresh).

      Returns:
          Callable[..., tuple[Response, int] | R]: Декорированная функция, которая возвращает кортеж из
                                                     `Response` и `int` (код состояния) или результат
                                                     декорируемой функции.

      Raises:
          AuthenticationError: Если заголовок авторизации отсутствует, не начинается с
                               `TOKEN_STARTSWITH_BEARER`, или если токен недействителен.
      """

    def login_jwt_required_decorator(func: Callable[..., R]) -> Callable[..., tuple[Response, int] | R]:

        @wraps(func)
        def wrapped(self: JWTMixin, *args, **kwargs) -> tuple[Response, int] | R:
            try:
                auth_header = request.headers.get(AUTH_HEADER)
                if not auth_header:
                    raise AuthenticationError()
                if not auth_header.startswith(TOKEN_STARTSWITH_BEARER):
                    raise AuthenticationError(MESSAGE_TOKEN_INVALID_401)
                token = auth_header.split()[1]
                payload_data = self._decode_jwt(token=token, exc=AuthenticationError, message=MESSAGE_TOKEN_INVALID_401)
                get_payload = JWTPayloadSchema(**payload_data)
                if not get_payload.type == type_token:
                    raise AuthenticationError(MESSAGE_TOKEN_INVALID_401)
            except (ValidationError, AuthenticationError) as e:
                return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 401
            else:
                return func(self, token, *args, **kwargs)

        return wrapped

    return login_jwt_required_decorator
