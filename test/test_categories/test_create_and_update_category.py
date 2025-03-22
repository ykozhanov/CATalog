import pytest

from src.backend.core.decorators.base64_login import AUTH_HEADER

from test.utils import APIPathsEnum, set_bearer_token_prefix
from test.models import test_category, test_update_category


@pytest.mark.order(2)
def test_success_create_category(client, jwt_tokens):
    bearer_access_token = set_bearer_token_prefix(jwt_tokens.access_token)

    headers = {AUTH_HEADER: bearer_access_token}
    response = client.post(APIPathsEnum.CATEGORIES.value, headers=headers, json=test_category.dict())


    assert response.status_code == 201
    assert response.json.get("name") == test_category.name
