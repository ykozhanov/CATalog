from flask import jsonify, request, Response
from flask.views import MethodView
from pydantic import ValidationError

from src.db_lib.base.exceptions import NotFoundInDBError

from src.backend.core.utils import crud, session
from src.backend.core.decorators import login_jwt_required_decorator
from src.backend.core.mixins import JWTMixin
from src.backend.core.response.schemas import ErrorMessageSchema
from src.backend.core.database.models import User
from src.backend.core.exceptions import ForbiddenError, BadRequestError
from src.backend.core.exceptions.messages import MESSAGE_BAD_REQUEST_ERROR_400

from .schemas import CategoryInSchema, CategoryOutSchema, CategoryListOutSchema
from .models import Category

QUERY_STRING_DELETE_ALL_PRODUCTS = "delete_all_products"


class CategoriesMethodView(JWTMixin, MethodView):
    model = Category
    element_in_schema = CategoryInSchema
    element_out_schema = CategoryOutSchema
    element_list_out_schema = CategoryListOutSchema
    attr_for_list_out_schema = "categories"

    @login_jwt_required_decorator
    def get(self, current_user: User) -> tuple[Response, int]:
        result = current_user.profile.categories
        return (
            jsonify(
                self.element_list_out_schema.model_validate({self.attr_for_list_out_schema: result})
                .model_dump()
            ),
            200,
        )

    @login_jwt_required_decorator
    def post(self, current_user: User) -> tuple[Response, int]:
        try:
            new_element_validated = self.element_in_schema.model_validate_json(request.get_json())
            if crud.where(self.model, "name", new_element_validated.name):
                raise BadRequestError(
                    f"{MESSAGE_BAD_REQUEST_ERROR_400}: Категория {new_element_validated.name} уже существует"
                )
            new_element_model = self.model(profile_id=current_user.profile.id, **new_element_validated.model_dump())
            new_element = crud.create(new_element_model)
        except (ValidationError, BadRequestError) as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 400
        else:
            return jsonify(dict(self.element_out_schema.model_validate(new_element))), 201


class CategoriesByIDMethodView(JWTMixin, MethodView):
    model = Category
    element_in_schema = CategoryInSchema
    element_out_schema = CategoryOutSchema
    element_list_out_schema = CategoryListOutSchema

    @login_jwt_required_decorator
    def get(self, current_user: User, category_id: int) -> tuple[Response, int]:
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
            return jsonify(dict(self.element_out_schema.model_validate(element))), 200

    @login_jwt_required_decorator
    def put(self, current_user: User, category_id: int) -> tuple[Response, int]:
        try:
            old_element = crud.read(self.model, pk=category_id)
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
        except ValidationError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 400
        except ForbiddenError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 403
        except NotFoundInDBError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 404
        else:
            return jsonify(dict(self.element_out_schema.model_validate(update_element))), 200

    @login_jwt_required_decorator
    def delete(self, current_user: User, category_id: int) -> tuple[Response, int]:
        try:
            delete_all_products = request.args.get(QUERY_STRING_DELETE_ALL_PRODUCTS, "false").lower() == "true"
            old_element = crud.read(self.model, pk=category_id)
            if old_element is None:
                raise NotFoundInDBError()
            if old_element.profile_id != current_user.profile.id:
                raise ForbiddenError()
            db_session = session.session()
            with db_session as s:
                if delete_all_products:
                    for product in old_element.products:
                        s.delete(product)
                s.delete(old_element)
                s.commit()
        except BadRequestError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 400
        except ForbiddenError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 403
        except NotFoundInDBError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 404
        else:
            return jsonify(), 204
