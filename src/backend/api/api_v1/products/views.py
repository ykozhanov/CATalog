import re
import json
from datetime import datetime, UTC

from flask import jsonify, request, Response
from flask.views import MethodView
from pydantic import ValidationError, BaseModel

from src.db_lib.base.exceptions import NotFoundInDBError, IntegrityDBError
from src.db_lib.base.exceptions.messages import MESSAGE_INTEGRITY_ERROR

from src.backend.core.utils import crud, session as S
from src.backend.core.mixins import JWTMixin
from src.backend.core.decorators import login_jwt_required_decorator
from src.backend.core.response.schemas import ErrorMessageSchema
from src.backend.core.database.models import User, Base
from src.backend.core.exceptions import ForbiddenError
from src.backend.core.database import redis_cache
from src.backend.settings import CACHE_TIME_SEC

from .schemas import ProductInSchema, ProductOutSchema, ProductListOutSchema
from .models import Product

QUERY_STRING_SEARCH_BY_NAME = "name"
QUERY_STRING_SEARCH_BY_CATEGORY_ID = "category_id"
QUERY_STRING_SEARCH_BY_EXP_DAYS = "exp_days"


class RedisCacheProductMixin:
    @staticmethod
    def del_cache_by_name_or_category_id(
            current_user: User,
            prefix: str,
            name: str | None = None,
            category_id: int | None = None,
    ) -> None:
        if name is None and category_id is None:
            return None
        if name:
            cache_key_name = f"{prefix}_{QUERY_STRING_SEARCH_BY_NAME}:{name}:{current_user.profile.id}"
            redis_cache.delete(cache_key_name)
        if category_id:
            cache_key_category_id = f"{prefix}_{QUERY_STRING_SEARCH_BY_CATEGORY_ID}:{category_id}:{current_user.profile.id}"
            redis_cache.delete(cache_key_category_id)

    @staticmethod
    def get_json_list_for_cache(model: type[BaseModel], data: list[Base]) -> str:
        return json.dumps([model.model_validate(e).model_dump_json() for e in data])

    @staticmethod
    def get_model_list_from_cache(model: type[BaseModel], data: str) -> list[BaseModel]:
        return [model.model_validate_json(e) for e in json.loads(data)]


class ProductsMethodView(RedisCacheProductMixin, JWTMixin, MethodView):
    model = Product
    element_in_schema = ProductInSchema
    element_out_schema = ProductOutSchema
    element_list_out_schema = ProductListOutSchema
    attr_for_list_out_schema = "products"

    def _get_products_by_name(self, name: str, current_user: User) -> list[element_out_schema]:
        cache_key = f"{self.attr_for_list_out_schema}_{QUERY_STRING_SEARCH_BY_NAME}:{name}:{current_user.profile.id}"
        if data := redis_cache.get(cache_key):
            return self.get_model_list_from_cache(model=self.element_out_schema, data=data)
        pattern = rf"(?i).*{re.escape(name)}.*"
        filters = {"name": QUERY_STRING_SEARCH_BY_NAME, "profile_id": current_user.profile.id}
        data = crud.re(model=self.model, main_attr=QUERY_STRING_SEARCH_BY_NAME, filters=filters, pattern=pattern)
        redis_cache.setex(cache_key, CACHE_TIME_SEC, self.get_json_list_for_cache(model=self.element_out_schema, data=data))
        return [self.element_out_schema.model_validate(e) for e in data]

    def _get_products_by_category_id(self, category_id: int, current_user: User) -> list[element_out_schema]:
        cache_key = f"{self.attr_for_list_out_schema}_{QUERY_STRING_SEARCH_BY_CATEGORY_ID}:{category_id}:{current_user.profile.id}"
        if data := redis_cache.get(cache_key):
            return self.get_model_list_from_cache(model=self.element_out_schema, data=data)
        session = S.session()
        with session as s:
            data = s.query(self.model).filter(
                self.model.category_id == category_id,
                self.model.profile_id == current_user.profile.id,
            ).all()
        redis_cache.setex(cache_key, CACHE_TIME_SEC, self.get_json_list_for_cache(model=self.element_out_schema, data=data))
        return [self.element_out_schema.model_validate(e) for e in data]

    def _get_products_by_exp_days(self, exp_days: int, current_user: User) -> list[element_out_schema]:
        now = datetime.now(UTC).date()
        session = S.session()
        with session as s:
            data = s.query(self.model).filter(
                self.model.exp_date - now <= exp_days,
                self.model.profile_id == current_user.profile.id,
            ).all()
        return [self.element_out_schema.model_validate(e) for e in data]

    @login_jwt_required_decorator
    def get(self, current_user: User) -> tuple[Response, int]:
        try:
            if name := request.args.get(QUERY_STRING_SEARCH_BY_NAME):
                result = self._get_products_by_name(name, current_user)
            elif category_id := request.args.get(QUERY_STRING_SEARCH_BY_CATEGORY_ID, type=int):
                if category_id not in (c.id for c in current_user.profile.categories):
                    raise ForbiddenError()
                result = self._get_products_by_category_id(category_id, current_user)
            elif exp_days := request.args.get(QUERY_STRING_SEARCH_BY_EXP_DAYS, type=int):
                result = self._get_products_by_exp_days(exp_days, current_user)
            else:
                result = [self.element_out_schema.model_validate(e) for e in current_user.profile.products]
            result = [] if not result else result
            data_for_list_out_schema = {
                self.attr_for_list_out_schema: result,
            }
        except ForbiddenError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 403
        else:
            return jsonify(self.element_list_out_schema(**data_for_list_out_schema).model_dump()), 200

    @login_jwt_required_decorator
    def post(self, current_user: User) -> tuple[Response, int]:
        try:
            new_element_validated = self.element_in_schema.model_validate_json(request.get_json())
            all_categories = [category.id for category in current_user.profile.categories]
            if new_element_validated.category_id not in all_categories:
                raise IntegrityDBError(f"{MESSAGE_INTEGRITY_ERROR}: Указанной категории не существует")
            new_element_model = self.model(profile_id=current_user.profile.id, **new_element_validated.model_dump())
            self.del_cache_by_name_or_category_id(
                current_user,
                prefix=self.attr_for_list_out_schema,
                name=new_element_model.name,
                category_id=new_element_model.category_id,
            )
            new_element = crud.create(new_element_model)
        except (ValidationError, IntegrityDBError) as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 400
        else:
            return jsonify(dict(self.element_out_schema.model_validate(new_element))), 201


class ProductsByIDMethodView(RedisCacheProductMixin, JWTMixin, MethodView):
    model = Product
    element_in_schema = ProductInSchema
    element_out_schema = ProductOutSchema
    element_list_out_schema = ProductListOutSchema
    attr_for_list_out_schema = "products"

    @login_jwt_required_decorator
    def get(self, current_user: User, product_id: int) -> tuple[Response, int]:
        try:
            element = crud.read(model=self.model, pk=product_id)
            if element is None:
                raise NotFoundInDBError()
            if element.profile_id != current_user.profile.id:
                raise ForbiddenError()
        except ForbiddenError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 403
        except NotFoundInDBError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 404
        else:
            return jsonify(dict(self.element_out_schema.model_validate(element))), 200

    @login_jwt_required_decorator
    def put(self, current_user: User, product_id: int) -> tuple[Response, int]:
        try:
            old_element = crud.read(self.model, pk=product_id)
            if old_element is None:
                raise NotFoundInDBError()
            if old_element.profile_id != current_user.profile.id:
                raise ForbiddenError()
            update_element_validated = self.element_in_schema.model_validate_json(request.get_json())
            update_element = crud.update(
                model=self.model,
                pk=old_element.id,
                obj_data=update_element_validated.model_dump(),
            )
            self.del_cache_by_name_or_category_id(
                current_user,
                prefix=self.attr_for_list_out_schema,
                name=old_element.name,
                category_id=old_element.category_id,
            )
            if update_element:
                result = jsonify(dict(self.element_out_schema.model_validate(update_element))), 200
            else:
                result = jsonify(), 204
        except ValidationError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 400
        except ForbiddenError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 403
        except NotFoundInDBError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 404
        else:
            return result

    @login_jwt_required_decorator
    def delete(self, current_user: User, product_id: int) -> tuple[Response, int]:
        try:
            old_element = crud.read(self.model, pk=product_id)
            if old_element is None:
                raise NotFoundInDBError()
            if old_element.profile_id != current_user.profile.id:
                raise ForbiddenError()
            crud.delete(self.model, pk=old_element.id)
            self.del_cache_by_name_or_category_id(
                current_user,
                prefix=self.attr_for_list_out_schema,
                name=old_element.name,
                category_id=old_element.category_id,
            )
        except ForbiddenError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 403
        except NotFoundInDBError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 404
        else:
            return jsonify(), 204
