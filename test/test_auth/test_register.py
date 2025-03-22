import pytest

from src.backend.core.decorators.base64_login import AUTH_HEADER

from test.utils import APIPathsEnum, register_credential_base64_encode, set_basic_token_prefix
from test.models import test_user


@pytest.mark.order(1)
def test_success_register_user(client):
    credential_base64 = register_credential_base64_encode(test_user)
    basic_token = set_basic_token_prefix(credential_base64)

    headers = {AUTH_HEADER: basic_token}
    response = client.post(APIPathsEnum.REGISTER.value, headers=headers)
    response_data: dict = response.json

    assert response.status_code == 201
    assert response_data.get("access_token") is not None
    assert response_data.get("refresh_token") is not None
