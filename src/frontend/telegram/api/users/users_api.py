import requests
from pydantic import ValidationError

from src.frontend.telegram.core.exceptions.messages import (
    MESSAGE_CREATE_USER_ERROR,
    MESSAGE_GET_TOKEN_ERROR,
    MESSAGE_AUTHENTICATION_ERROR,
)
from src.frontend.telegram.core.exceptions import CreateUserError, AuthenticationError, GetTokenError
from src.frontend.telegram.core.request import BearerAuth
from src.frontend.telegram.settings import BACKEND_URL
from .schemas import UserInSchema


class UsersAPI:
    _token_bearer = "Bearer"
    _token_basic = "Basic"

    _api_prefix_login = "/users/login/"
    _api_prefix_register = "/users/register/"
    _api_prefix_token = "/users/token/"

    @classmethod
    def login_or_register(cls, username: str, password: str, register_email: str | None = None) -> UserInSchema:
        if register_email:
            credentials = (username, password, register_email)
        else:
            credentials = (username, password)
        url = f"{BACKEND_URL}{cls._api_prefix_register if register_email else cls._api_prefix_login}"
        response = requests.post(url, auth=credentials)

        try:
            if response.ok:
                return UserInSchema(**response.json())
            else:
                raise CreateUserError(f"{MESSAGE_CREATE_USER_ERROR}: {response.text}")
        except (ValidationError, CreateUserError) as e:
            raise CreateUserError(str(e))

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
                raise CreateUserError(f"{MESSAGE_GET_TOKEN_ERROR}: {response.text}")
        except (ValidationError, AuthenticationError, GetTokenError) as e:
            raise CreateUserError(str(e))
