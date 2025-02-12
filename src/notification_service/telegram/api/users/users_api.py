import requests
from pydantic import ValidationError

from src.notification_service.telegram.api.utils.bearer_util import BearerAuth
from src.notification_service.telegram.settings import settings

from .schemas import UserInSchema
from .exceptions import AuthenticationError, MESSAGE_AUTHENTICATION_ERROR, GetTokenError, MESSAGE_GET_TOKEN_ERROR


class UsersAPI:
    _api_prefix_token = "/users/token/"

    @classmethod
    def token(cls, refresh_jwt_token: str) -> UserInSchema:
        url = f"{settings.backend_url}{cls._api_prefix_token}"
        response = requests.post(url, auth=BearerAuth(refresh_jwt_token))

        try:
            if response.ok:
                data = response.json()
                return UserInSchema(**data)
            elif response.status_code == 401:
                raise AuthenticationError(f"{MESSAGE_AUTHENTICATION_ERROR}: {response.text}")
            else:
                raise GetTokenError(f"{MESSAGE_GET_TOKEN_ERROR}: {response.text}")
        except ValidationError as e:
            raise GetTokenError(str(e))
