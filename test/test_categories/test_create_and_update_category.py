import pytest

from test.utils import APIPathsEnum
from test.models import test_category, test_update_category


@pytest.mark.order(2)
def test_success_create_category(client, access_token_headers):
    response = client.post(APIPathsEnum.CATEGORIES.value, headers=access_token_headers, json=test_category.to_json())

    assert response.status_code == 201
    assert response.json.get("name") == test_category.name
    assert response.json.get("id") == test_category.id


@pytest.mark.order(3)
def test_success_update_category(client, access_token_headers):
    url_with_category_id = f"{APIPathsEnum.CATEGORIES.value}{test_category.id}/"
    response = client.put(url_with_category_id, headers=access_token_headers, json=test_update_category.to_json())

    assert response.status_code == 200
    assert response.json.get("name") == test_update_category.name
    assert response.json.get("id") == test_category.id
