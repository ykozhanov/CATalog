import json
import logging

import requests
from pydantic import ValidationError

from src.frontend.telegram.core.exceptions.messages import MESSAGE_AUTHENTICATION_ERROR
from src.frontend.telegram.core.exceptions import AuthenticationError
from src.frontend.telegram.core.request import BearerAuth
from src.frontend.telegram.settings import BACKEND_URL
from src.frontend.telegram.api.exc_crud_messages import (
    MESSAGE_POST_ERROR,
    MESSAGE_GET_ERROR,
    MESSAGE_DELETE_ERROR,
    MESSAGE_PUT_ERROR,
)
from .schemas import CategoryInSchema, CategoryInListSchema, CategoryOutSchema
from .exceptions import CategoryError, MESSAGE_CATEGORY_ERROR

QUERY_STRING_DELETE_ALL_PRODUCTS = "delete_all_products"


class CategoriesAPI:
    _api_prefix = "/categories/"
    _url = f"{BACKEND_URL}{_api_prefix}"

    _main_exc = CategoryError
    _main_message_error = MESSAGE_CATEGORY_ERROR
    _element_in_schema = CategoryInSchema
    _element_in_list_schema = CategoryInListSchema
    _element_out_schema = CategoryOutSchema
    _attr_for_list_out_schema = "categories"

    def __init__(self, access_token: str):
        self._access_token = access_token

    def post(self, element: _element_out_schema) -> None:
        response = requests.post(self._url, auth=BearerAuth(self._access_token), json=element.model_dump_json())
        try:
            if response.status_code == 401:
                raise AuthenticationError(f"{MESSAGE_AUTHENTICATION_ERROR}: {json.dumps(response.json(), ensure_ascii=False)}")
            elif not response.ok:
                raise self._main_exc(f"{self._main_message_error}. {MESSAGE_POST_ERROR}: {json.dumps(response.json(), ensure_ascii=False)}")
        except (ValidationError, self._main_exc) as e:
            raise self._main_exc(str(e))

    def get_all(self) -> list[_element_in_schema]:
        logging.info("Старт 'CategoriesAPI -> get_all'")
        response = requests.get(self._url, auth=BearerAuth(self._access_token))
        logging.debug(f"response.json: {response.json()}")
        try:
            if response.ok:
                data = self._element_in_list_schema.model_validate(response.json())
                return getattr(data, self._attr_for_list_out_schema)
            if response.status_code == 401:
                logging.info("Конец 'CategoriesAPI -> get_all'")
                raise AuthenticationError(f"{MESSAGE_AUTHENTICATION_ERROR}: {json.dumps(response.json(), ensure_ascii=False)}")
            else:
                logging.info("Конец 'CategoriesAPI -> get_all'")
                raise self._main_exc(f"{self._main_message_error}. {MESSAGE_GET_ERROR}: {json.dumps(response.json(), ensure_ascii=False)}")
        except (ValidationError, self._main_exc) as e:
            logging.info("Конец 'CategoriesAPI -> get_all'")
            raise self._main_exc(str(e))

    def delete(self, element_id: int, delete_all_products: bool = False) -> None:
        params = {QUERY_STRING_DELETE_ALL_PRODUCTS: delete_all_products}
        response = requests.delete(f"{self._url}{element_id}", auth=BearerAuth(self._access_token), params=params)
        try:
            if response.status_code == 401:
                raise AuthenticationError(f"{MESSAGE_AUTHENTICATION_ERROR}: {json.dumps(response.json(), ensure_ascii=False)}")
            elif not response.ok:
                raise self._main_exc(f"{self._main_message_error}. {MESSAGE_DELETE_ERROR}: {json.dumps(response.json(), ensure_ascii=False)}")
        except (ValidationError, self._main_exc) as e:
            raise self._main_exc(str(e))

    def put(self, element_id: int, put_element: _element_out_schema) -> None:
        response = requests.put(f"{self._url}{element_id}", auth=BearerAuth(self._access_token), json=put_element.model_dump_json())
        try:
            if response.status_code == 401:
                raise AuthenticationError(f"{MESSAGE_AUTHENTICATION_ERROR}: {json.dumps(response.json(), ensure_ascii=False)}")
            elif not response.ok:
                raise self._main_exc(f"{self._main_message_error}. {MESSAGE_PUT_ERROR}: {json.dumps(response.json(), ensure_ascii=False)}")
        except (ValidationError, self._main_exc) as e:
            raise self._main_exc(str(e))
