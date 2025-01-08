import base64
from typing import Callable, TypeVar
from functools import wraps

from flask import request, jsonify, Response
from pydantic import ValidationError

from src.backend.core.settings_app import AUTH_HEADER
from src.backend.core.response import MESSAGE_TOKEN_INVALID_401, ErrorMessageSchema, MESSAGE_AUTHENTICATION_ERROR_401
from src.backend.core.request import TOKEN_STARTSWITH_BASIC
from src.backend.core.database.schemas import RegisterSchema
from src.backend.core.exceptions import AuthenticationError

R = TypeVar("R")


def base64_register_decorator(func: Callable[..., R]) -> Callable[..., tuple[Response, int] | R]:
    """Декоратор для обработки регистрации с использованием Base64.

        Этот декоратор извлекает заголовок авторизации из запроса, декодирует его из формата Base64
        и проверяет наличие имени пользователя, пароля и адреса электронной почты. Если данные корректны,
        они передаются в декорируемую функцию первым (позиционным) аргументом как pydantic схема `RegisterSchema`.

        Args:
            func (Callable[..., R]): Функция, которую декорирует данный декоратор.
                                      Ожидается, что она принимает `register_data` как первый аргумент (позиционный).

        Returns:
            Callable[..., tuple[Response, int] | R]: Обернутая функция, которая возвращает кортеж из
                                                       `Response` и `int` (код состояния) или результат
                                                       декорируемой функции.

        Raises:
            AuthenticationError: Если заголовок авторизации отсутствует, не начинается с
                                 `TOKEN_STARTSWITH_BASIC`, или если данные не могут быть декодированы.
        """

    @wraps(func)
    def wrapped(self, *args, **kwargs) -> tuple[Response, int] | R:
        try:
            auth_header = request.headers.get(AUTH_HEADER)
            if not auth_header:
                raise AuthenticationError(MESSAGE_AUTHENTICATION_ERROR_401)
            if not auth_header.startswith(TOKEN_STARTSWITH_BASIC):
                raise AuthenticationError(MESSAGE_TOKEN_INVALID_401)
            register_get_data = base64.b64decode(auth_header.split()[1]).decode("utf-8").split(":")
            if len(register_get_data) != 3:
                raise AuthenticationError(MESSAGE_TOKEN_INVALID_401)
            username, password, email = register_get_data
            register_data = RegisterSchema(username=username, password=password, email=email)
        except (ValidationError, AuthenticationError) as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 401
        else:
            return func(self, register_data, *args, **kwargs)

    return wrapped
