from test.utils import (
    APIPathsEnum,
    login_credential_base64_encode,
    set_basic_token_prefix,
    set_bearer_token_prefix,
)

from test.models import test_user
from src.backend.core.decorators.base64_login import AUTH_HEADER


def test_success_login_user(client):
    credential_base64 = login_credential_base64_encode(test_user)
    basic_token = set_basic_token_prefix(credential_base64)

    headers = {AUTH_HEADER: basic_token}
    response = client.post(APIPathsEnum.LOGIN.value, headers=headers)
    response_data: dict = response.json

    assert response.status_code == 200
    assert response_data.get("access_token") is not None
    assert response_data.get("refresh_token") is not None



def test_success_get_access_token(client, jwt_tokens):
    bearer_refresh_token = set_bearer_token_prefix(jwt_tokens.refresh_token)

    headers = {AUTH_HEADER: bearer_refresh_token}
    response = client.post(APIPathsEnum.TOKEN.value, headers=headers)

    assert response.status_code == 200
    assert response.json.get("access_token") is not None
    assert response.json.get("refresh_token") is not None
