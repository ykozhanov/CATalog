from typing import Callable, TypeVar
from functools import wraps

from flask import request, jsonify, Response
from pydantic import ValidationError

from src.backend.settings import USER_MODEL
from src.backend.core.mixins import JWTMixin
from src.backend.core.exceptions import AuthenticationError
from src.backend.core.exceptions.messages import MESSAGE_TOKEN_INVALID_401
from src.backend.core.settings_app import AUTH_HEADER
from src.backend.core.utils import crud
from src.backend.core.response import ErrorMessageSchema
from src.backend.core.request import TOKEN_STARTSWITH_BEARER, JWTPayloadSchema, TYPE_ACCESS_JWT

R = TypeVar("R")


def login_jwt_required_decorator(func: Callable[..., R]) -> Callable[..., tuple[Response, int] | R]:
    """Декоратор для проверки JWT токена при входе пользователя.

        Этот декоратор извлекает заголовок авторизации из запроса, проверяет его на наличие
        токена в формате Bearer и декодирует его. Если токен валиден и соответствует ожидаемому
        типу, он извлекает информацию о текущем пользователе и передает ее в декорируемую функцию
        первым (позиционным) аргументом как экземпляр SQLAlchemy модели `USER_MODEL`.

        Args:
            func (Callable[..., R]): Функция, которую декорирует данный декоратор.
                                      Ожидается, что она принимает `current_user` как первый (позиционный) аргумент.

        Returns:
            Callable[..., tuple[Response, int] | R]: Декорированная функция, которая возвращает кортеж из
                                                       `Response` и `int` (код состояния) или результат
                                                       декорируемой функции.

        Raises:
            AuthenticationError: Если заголовок авторизации отсутствует, не начинается с
                                 `TOKEN_STARTSWITH_BEARER`, токен недействителен, или если
                                 пользователь не найден.
        """

    @wraps(func)
    def wrapped(self: JWTMixin, *args, **kwargs) -> tuple[Response, int] | R:
        try:
            auth_header = request.headers.get(AUTH_HEADER)
            if not auth_header:
                raise AuthenticationError()
            if not auth_header.startswith(TOKEN_STARTSWITH_BEARER):
                raise AuthenticationError(MESSAGE_TOKEN_INVALID_401)
            payload_data = self._decode_jwt(token=auth_header.split()[1], exc=AuthenticationError, message=MESSAGE_TOKEN_INVALID_401)
            payload = JWTPayloadSchema(**payload_data)
            if not payload.type == TYPE_ACCESS_JWT:
                raise AuthenticationError(MESSAGE_TOKEN_INVALID_401)
            user_id = int(payload.sub)
            current_user = crud.read(USER_MODEL, user_id)   # type: ignore
            if not current_user:
                raise AuthenticationError()
        except (ValidationError, AuthenticationError) as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 401
        else:
            return func(self, current_user, *args, **kwargs)

    return wrapped
