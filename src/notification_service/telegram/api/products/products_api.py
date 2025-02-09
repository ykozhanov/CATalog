import requests
from pydantic import ValidationError

from src.notification_service.telegram.api.users.exceptions import AuthenticationError, MESSAGE_AUTHENTICATION_ERROR
from src.notification_service.telegram.api.utils.bearer_util import BearerAuth
from src.notification_service.telegram.settings import Settings

from .schemas import ProductInSchema, ProductInListSchema, ProductOutSchema
from .exceptions import ProductError, MESSAGE_PRODUCT_ERROR, MESSAGE_GET_ERROR

QUERY_STRING_SEARCH_BY_EXP_DAYS = "exp_days"


class ProductsAPI:
    _api_prefix = "/products/"
    _url = f"{Settings.backend_url}{_api_prefix}"

    _main_exc = ProductError
    _main_message_error = MESSAGE_PRODUCT_ERROR
    _element_in_schema = ProductInSchema
    _element_in_list_schema = ProductInListSchema
    _element_out_schema = ProductOutSchema
    _attr_for_list_out_schema = "products"

    def __init__(self, access_token: str):
        self._access_token = access_token

    def get_by(self, exp_days: int = Settings.exp_days) -> list[_element_in_schema]:
        params = {QUERY_STRING_SEARCH_BY_EXP_DAYS: exp_days}

        response = requests.get(self._url, auth=BearerAuth(self._access_token), params=params)
        try:
            if response.ok:
                data_for_list = {
                    self._attr_for_list_out_schema: [self._element_in_schema(**e) for e in response.json()],
                }
                return self._element_in_list_schema(**data_for_list).products
            if response.status_code == 401:
                raise AuthenticationError(f"{MESSAGE_AUTHENTICATION_ERROR}: {response.text}")
            else:
                raise self._main_exc(f"{self._main_message_error}. {MESSAGE_GET_ERROR}: {response.text}")
        except (ValidationError, self._main_exc) as e:
            raise self._main_exc(str(e))
