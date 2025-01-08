import base64
from typing import Callable, TypeVar
from functools import wraps

from flask import request, jsonify
from flask.typing import Response
from pydantic import ValidationError

from src.backend.core.settings_app import AUTH_HEADER
from src.backend.core.response import ErrorMessageSchema
from src.backend.core.request import TOKEN_STARTSWITH_BASIC
from src.backend.core.database.schemas import LoginSchema
from src.backend.core.exceptions import AuthenticationError
from src.backend.core.exceptions.messages import MESSAGE_TOKEN_INVALID_401

R = TypeVar("R")


def base64_login_decorator(func: Callable[..., R]) -> Callable[..., tuple[Response, int] | R]:
    """Декоратор для обработки авторизации с использованием Base64.

    Этот декоратор извлекает заголовок авторизации из запроса, декодирует его из формата Base64
    и проверяет наличие имени пользователя и пароля. Если данные корректны, они передаются в декорируемую функцию
    первым (позиционным) аргументом как pydantic схема `LoginSchema`.

    Args:
        func (Callable[..., R]): Функция, которую декорирует данный декоратор.
                                  Ожидается, что она принимает `login_data` как первый аргумент (позиционный).

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
                raise AuthenticationError()
            if not auth_header.startswith(TOKEN_STARTSWITH_BASIC):
                raise AuthenticationError(MESSAGE_TOKEN_INVALID_401)
            login_get_data = base64.b64decode(auth_header.split()[1]).decode("utf-8").split(":")
            if len(login_get_data) != 2:
                raise AuthenticationError(MESSAGE_TOKEN_INVALID_401)
            username, password = login_get_data
            login_data = LoginSchema(username=username, password=password)
        except (ValidationError, AuthenticationError) as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 401
        else:
            return func(self, login_data, *args, **kwargs)

    return wrapped
