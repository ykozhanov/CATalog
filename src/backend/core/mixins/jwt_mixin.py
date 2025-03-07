import uuid
import os
from datetime import datetime, timedelta, UTC
from typing import Any

import jwt

# from src.backend.core.settings_app import JWT_PRIVATE_KEY, JWT_PUBLIC_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from src.backend.core.request import JWTPayloadSchema, TYPE_ACCESS_JWT, TYPE_REFRESH_JWT
from src.backend.core.exceptions import AuthenticationError, ENVError
from src.backend.core.exceptions.messages import MESSAGE_TOKEN_INVALID_401, MESSAGE_ENV_ERROR

'''
Для генерации RSA ключей используйте команды:

`openssl genrsa -out jwt-private.pem 2048`
Эта команда генерирует закрытый ключ RSA длиной 2048 бит и сохраняет его в файл jwt-private.pem.

`openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem`
Эта команда извлекает открытый ключ из ранее сгенерированного закрытого ключа, который хранится в файле jwt-private.pem.
'''

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))

JWT_PRIVATE_KEY = os.getenv("JWT_PRIVATE_KEY")
JWT_PUBLIC_KEY = os.getenv("JWT_PUBLIC_KEY")
if not JWT_PUBLIC_KEY or not JWT_PRIVATE_KEY:
    raise ENVError(f"{MESSAGE_ENV_ERROR}: установите JWT_PRIVATE_KEY и JWT_PUBLIC_KEY")

JWT_ALGORITHM = "RS256"


class JWTMixin:
    """Mixin для работы с JSON Web Tokens (JWT).

    Этот класс предоставляет методы для кодирования и декодирования JWT.
    Использует RSA ключи для подписи и проверки токенов.
    """

    @staticmethod
    def _encode_jwt(payload: dict[str, Any]) -> str:
        """Кодирует данные в JWT.

        Args:
            payload (dict[str, Any]): Данные, которые будут закодированы в токен.

        Returns:
            str: Закодированный JWT.
        """
        return jwt.encode(payload=payload, key=JWT_PRIVATE_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def _decode_jwt(token: str | bytes, exc: type[Exception], message: str) -> dict[str, Any]:
        """Декодирует JWT и проверяет его валидность.

        Args:
            token (str | bytes): JWT для декодирования.
            exc (Type[Exception]): Исключение, которое будет вызвано в случае ошибки.
            message (str): Сообщение об ошибке.

        Returns:
            dict[str, Any]: Декодированные данные из токена.

        Raises:
            exc: Если токен недействителен.
        """
        try:
            return jwt.decode(jwt=token, key=JWT_PUBLIC_KEY, algorithms=[JWT_ALGORITHM])
        except jwt.InvalidTokenError:
            raise exc(message)


class JWTWithGetTokenMixin(JWTMixin):
    """Mixin для получения JWT токенов.

    Этот класс расширяет функциональность JWTMixin, добавляя метод для получения
    access и refresh JWT токенов.
    """

    def _get_jwt_token(
            self,
            sub: str | int | None = None,
            refresh_token: str | bytes | None = None,
            exc: type[Exception] = AuthenticationError,
            message: str = MESSAGE_TOKEN_INVALID_401,
    ):
        """Получает JWT токен, создавая новый или извлекая из refresh токена:
            - для получения access токена нужно обязательно передать аргумент **refresh_token**. При необходимости можно передать `exc` и `message`;
            - для получения refresh токена нужно передать аргумент **sub**.

        Args:
            sub (str | int | None): Подписчик (subject) токена. Если None, будет извлечен из refresh токена.
            refresh_token (str | bytes | None): Refresh токен для извлечения данных.
            exc (Type[Exception]): Исключение, которое будет вызвано в случае ошибки, возникшей при декодировании refresh токена. Значение по умолчанию `AuthenticationError`.
            message (str): Сообщение об ошибке, возникшей при декодировании refresh токена. Значение по умолчанию `MESSAGE_TOKEN_INVALID_401`.

        Returns:
            str: Закодированный JWT токен.

        Raises:
            exc: Если refresh токен недействителен.
        """
        if refresh_token:
            payload_data = self._decode_jwt(token=refresh_token, exc=exc, message=message)
            payload_from_refresh: JWTPayloadSchema = JWTPayloadSchema(**payload_data)
            sub = payload_from_refresh.sub
            td = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        else:
            if not sub:
                raise AuthenticationError(MESSAGE_TOKEN_INVALID_401)
            td = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

        payload = JWTPayloadSchema(
            sub=sub,
            iat=datetime.now(UTC),
            exp=datetime.now() + td,
            jti=uuid.uuid4().hex,
            type=TYPE_ACCESS_JWT if refresh_token else TYPE_REFRESH_JWT,
        )
        return self._encode_jwt(payload=payload.model_dump())
