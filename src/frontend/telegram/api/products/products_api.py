import requests
from pydantic import ValidationError

from src.frontend.telegram.core.exceptions.messages import (
    MESSAGE_AUTHENTICATION_ERROR,
    MESSAGE_PRODUCT_ERROR,
    MESSAGE_POST_ERROR,
    MESSAGE_GET_ERROR,
    MESSAGE_DELETE_ERROR,
    MESSAGE_PUT_ERROR,
)
from src.frontend.telegram.core.exceptions import AuthenticationError, ProductError
from src.frontend.telegram.core.request import BearerAuth
from src.frontend.telegram.settings import BACKEND_URL, EXP_DAYS
from .schemas import ProductInSchema, ProductInListSchema, ProductOutSchema

QUERY_STRING_SEARCH_BY_NAME = "name"
QUERY_STRING_SEARCH_BY_CATEGORY_ID = "category_id"
QUERY_STRING_SEARCH_BY_EXP_DAYS = "exp_days"


class ProductsAPI:
    _token_bearer = "Bearer"
    _api_prefix = "/products/"
    _url = f"{BACKEND_URL}{_api_prefix}"

    _main_exc = ProductError
    _main_message_error = MESSAGE_PRODUCT_ERROR
    _element_in_schema = ProductInSchema
    _element_in_list_schema = ProductInListSchema
    _element_out_schema = ProductOutSchema
    _attr_for_list_out_schema = "products"

    def __init__(self, access_token: str):
        self._access_token = access_token

    def post(self, element: _element_out_schema) -> None:
        response = requests.post(self._url, auth=BearerAuth(self._access_token), json=element.model_dump_json())
        try:
            if response.status_code == 401:
                raise AuthenticationError(f"{MESSAGE_AUTHENTICATION_ERROR}: {response.text}")
            elif not response.ok:
                raise self._main_exc(f"{self._main_message_error}. {MESSAGE_POST_ERROR}: {response.text}")
        except (ValidationError, self._main_exc) as e:
            raise self._main_exc(str(e))

    def get_all(self) -> list[_element_in_schema]:
        response = requests.get(self._url, auth=BearerAuth(self._access_token))
        try:
            if response.ok:
                elements = [self._element_in_schema(**e) for e in response.json()]
                data = {
                    self._attr_for_list_out_schema: elements,
                }
                return getattr(self._element_in_list_schema(**data), self._attr_for_list_out_schema)
            if response.status_code == 401:
                raise AuthenticationError(f"{MESSAGE_AUTHENTICATION_ERROR}: {response.text}")
            else:
                raise self._main_exc(f"{self._main_message_error}. {MESSAGE_GET_ERROR}: {response.text}")
        except (ValidationError, self._main_exc) as e:
            raise self._main_exc(str(e))

    def get_by(
            self,
            name: str | None = None,
            category_id: int | None = None,
            exp_days: int = EXP_DAYS,
    ) -> _element_in_list_schema:
        if name:
            params = {QUERY_STRING_SEARCH_BY_NAME: name}
        elif category_id:
            params = {QUERY_STRING_SEARCH_BY_CATEGORY_ID: category_id}
        else:
            params = {QUERY_STRING_SEARCH_BY_EXP_DAYS: exp_days}

        response = requests.get(self._url, auth=BearerAuth(self._access_token), params=params)
        try:
            if response.ok:
                data_for_list = {
                    self._attr_for_list_out_schema: [self._element_in_schema(**e) for e in response.json()],
                }
                return self._element_in_list_schema(**data_for_list)
            if response.status_code == 401:
                raise AuthenticationError(f"{MESSAGE_AUTHENTICATION_ERROR}: {response.text}")
            else:
                raise self._main_exc(f"{self._main_message_error}. {MESSAGE_GET_ERROR}: {response.text}")
        except (ValidationError, self._main_exc) as e:
            raise self._main_exc(str(e))

    def delete(self, element_id: int) -> None:
        response = requests.delete(f"{self._url}{element_id}", auth=BearerAuth(self._access_token))
        try:
            if response.status_code == 401:
                raise AuthenticationError(f"{MESSAGE_AUTHENTICATION_ERROR}: {response.text}")
            elif not response.ok:
                raise self._main_exc(f"{self._main_message_error}. {MESSAGE_DELETE_ERROR}: {response.text}")
        except (ValidationError, self._main_exc) as e:
            raise self._main_exc(str(e))

    def put(self, element_id: int, put_element: _element_out_schema) -> None:
        response = requests.put(f"{self._url}{element_id}", auth=BearerAuth(self._access_token), json=put_element.model_dump_json())
        try:
            if response.status_code == 401:
                raise AuthenticationError(f"{MESSAGE_AUTHENTICATION_ERROR}: {response.text}")
            elif not response.ok:
                raise self._main_exc(f"{self._main_message_error}. {MESSAGE_PUT_ERROR}: {response.text}")
        except (ValidationError, self._main_exc) as e:
            raise self._main_exc(str(e))
