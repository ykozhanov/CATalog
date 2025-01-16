import re
from datetime import datetime, UTC

from flask import jsonify, request, Response
from flask.views import MethodView
from pydantic import ValidationError

from src.db_lib.base.exceptions import NotFoundInDBError

from src.backend.core.utils import crud, session as S
from src.backend.core.decorators import login_jwt_required_decorator
from src.backend.core.response.schemas import ErrorMessageSchema
from src.backend.settings import USER_MODEL, PROFILE_MODEL
from src.backend.core.exceptions import ForbiddenError

from .schemas import ProductInSchema, ProductOutSchema, ProductListOutSchema
from .models import Product

QUERY_STRING_SEARCH_BY_NAME = "name"
QUERY_STRING_SEARCH_BY_CATEGORY_ID = "category_id"
QUERY_STRING_SEARCH_BY_EXP_DAYS = "exp_days"


class ProductsMethodView(MethodView):
    model = Product
    element_in_schema = ProductInSchema
    element_out_schema = ProductOutSchema
    element_list_out_schema = ProductListOutSchema
    attr_for_list_out_schema = "products"

    def _get_products_by_name(self, name: str, current_user: USER_MODEL) -> list[model]:
        pattern = rf"(?i).*{re.escape(name)}.*"
        filters = {"name": QUERY_STRING_SEARCH_BY_NAME, "profile_id": current_user.profile.id}
        return crud.re(model=self.model, main_attr=QUERY_STRING_SEARCH_BY_NAME, filters=filters, pattern=pattern)

    def _get_products_by_category_id(self, category_id: int, current_user: USER_MODEL) -> list[model]:
        session = S.session()
        with session as s:
            return s.query(self.model).filter(
                self.model.category_id == category_id,
                self.model.profile_id == current_user.profile.id,
            ).all()

    def _get_products_by_exp_days(self, exp_days: int, current_user: USER_MODEL) -> list[model]:
        now = datetime.now(UTC).date()
        session = S.session()
        with session as s:
            return s.query(self.model).filter(
                self.model.exp_date - now <= exp_days,
                self.model.profile_id == current_user.profile.id,
            ).all()

    @login_jwt_required_decorator
    def get(self, current_user: USER_MODEL) -> tuple[Response, int]:
        try:
            if name := request.args.get(QUERY_STRING_SEARCH_BY_NAME):
                result = self._get_products_by_name(name, current_user)
            elif category_id := request.args.get(QUERY_STRING_SEARCH_BY_CATEGORY_ID, type=int):
                if category_id not in (c for c in current_user.profile.categories):
                    raise ForbiddenError()
                result = self._get_products_by_category_id(category_id, current_user)
            elif exp_days := request.args.get(QUERY_STRING_SEARCH_BY_EXP_DAYS, type=int):
                result = self._get_products_by_exp_days(exp_days, current_user)
            else:
                profile: PROFILE_MODEL = getattr(current_user, "profile")
                result = getattr(profile, self.attr_for_list_out_schema)
            data_for_list_out_schema = {
                self.attr_for_list_out_schema: [self.element_out_schema.model_validate(element) for element in result],
            }
        except ForbiddenError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 403
        else:
            return jsonify(self.element_list_out_schema(**data_for_list_out_schema).model_dump()), 200

    @login_jwt_required_decorator
    def post(self, current_user: USER_MODEL) -> tuple[Response, int]:
        try:
            new_element_data = request.get_json()
            new_element_validated = self.element_in_schema(**new_element_data)
            new_element_model = self.model(profile_id=current_user.profile.id, **new_element_validated.model_dump())
            new_element = crud.create(new_element_model)
        except ValidationError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 400
        else:
            return jsonify(self.element_out_schema.model_validate(new_element)), 201


class ProductsByIDMethodView(MethodView):
    model = Product
    element_in_schema = ProductInSchema
    element_out_schema = ProductOutSchema
    element_list_out_schema = ProductListOutSchema

    @login_jwt_required_decorator
    def get(self, current_user: USER_MODEL, category_id: int) -> tuple[Response, int]:
        try:
            element = crud.read(model=self.model, pk=category_id)
            if element is None:
                raise NotFoundInDBError()
            if element.profile_id != current_user.profile.id:
                raise ForbiddenError()
        except ForbiddenError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 403
        except NotFoundInDBError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 404
        else:
            return jsonify(self.element_out_schema.model_validate(element)), 200

    @login_jwt_required_decorator
    def put(self, current_user: USER_MODEL, category_id: int) -> tuple[Response, int]:
        try:
            old_element = crud.read(self.model, pk=category_id)
            if old_element is None:
                raise NotFoundInDBError()
            if old_element.profile_id != current_user.profile.id:
                raise ForbiddenError()
            update_element_data = request.get_json()
            update_element_validated = self.element_in_schema(**update_element_data)
            update_element = crud.update(
                model=self.model,
                pk=old_element.id,
                obj_data=update_element_validated.model_dump(),
            )
        except ValidationError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 400
        except ForbiddenError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 403
        except NotFoundInDBError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 404
        else:
            return jsonify(self.element_out_schema.model_validate(update_element)), 200

    @login_jwt_required_decorator
    def delete(self, current_user: USER_MODEL, category_id: int) -> tuple[Response, int]:
        try:
            old_element = crud.read(self.model, pk=category_id)
            if old_element is None:
                raise NotFoundInDBError()
            if old_element.profile_id != current_user.profile.id:
                raise ForbiddenError()
            crud.delete(self.model, pk=old_element.id)
        except ForbiddenError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 403
        except NotFoundInDBError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 404
        else:
            return jsonify(), 204
