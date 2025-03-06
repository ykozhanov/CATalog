import requests
import base64

from pydantic import ValidationError

from src.frontend.telegram.core.exceptions import AuthenticationError
from src.frontend.telegram.core.exceptions.messages import MESSAGE_AUTHENTICATION_ERROR
from src.frontend.telegram.core.request import BearerAuth
from src.frontend.telegram.settings import BACKEND_URL

from .schemas import UserInSchema
from .exceptions import CreateOrGetUserError, MESSAGE_CREATE_USER_ERROR, MESSAGE_GET_TOKEN_ERROR


def create_base_token(username: str, password: str, register_email: str | None = None):
    if register_email:
        for_encode = f"{username}:{password}:{register_email}".encode("utf-8")
    else:
        for_encode = f"{username}:{password}".encode("utf-8")
    return base64.b64encode(for_encode).decode("utf-8")


class UsersAPI:
    _api_prefix_login = "/users/login/"
    _api_prefix_register = "/users/register/"
    _api_prefix_token = "/users/token/"

    @classmethod
    def login_or_register(cls, username: str, password: str, register_email: str | None = None) -> UserInSchema:
        headers = {"Authorization": f"Basic {create_base_token(username, password, register_email)}"}
        url = f"{BACKEND_URL}{cls._api_prefix_register if register_email else cls._api_prefix_login}"
        response = requests.post(url, headers=headers)

        try:
            if response.ok:
                return UserInSchema(**response.json())
            else:
                raise CreateOrGetUserError(f"{MESSAGE_CREATE_USER_ERROR}: {response.text}")
        except ValidationError as e:
            raise CreateOrGetUserError(str(e))

    @classmethod
    def token(cls, refresh_jwt_token: str) -> UserInSchema:
        url = f"{BACKEND_URL}{cls._api_prefix_token}"
        response = requests.post(url, auth=BearerAuth(refresh_jwt_token))

        try:
            if response.ok:
                data = response.json()
                return UserInSchema(**data)
            elif response.status_code == 401:
                raise AuthenticationError(f"{MESSAGE_AUTHENTICATION_ERROR}: {response.text}")
            else:
                raise CreateOrGetUserError(f"{MESSAGE_GET_TOKEN_ERROR}: {response.text}")
        except ValidationError as e:
            raise CreateOrGetUserError(str(e))
