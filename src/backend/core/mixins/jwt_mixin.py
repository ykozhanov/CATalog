from typing import Any, Type

import jwt

from ..settings.settings_app import JWT_PRIVATE_KEY, JWT_PUBLIC_KEY, JWT_ALGORITHM

'''
Для генерации ключей используйте команды:

`openssl genrsa -out jwt-private.pem 2048`
Эта команда генерирует закрытый ключ RSA длиной 2048 бит и сохраняет его в файл jwt-private.pem.

`openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem`
Эта команда извлекает открытый ключ из ранее сгенерированного закрытого ключа, который хранится в файле jwt-private.pem.
'''


class JWTMixin:

    @staticmethod
    def _encode_jwt(payload: dict[str, Any]) -> str:
        return jwt.encode(payload=payload, key=JWT_PRIVATE_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def _decode_jwt(token: str | bytes, exc: Type[Exception]) -> dict[str, Any]:
        try:
            return jwt.decode(jwt=token, key=JWT_PUBLIC_KEY, algorithms=[JWT_ALGORITHM])
        except jwt.InvalidTokenError:
            raise exc()
