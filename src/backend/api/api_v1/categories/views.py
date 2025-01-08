from flask import jsonify, request, Response
from flask.views import MethodView
from pydantic import ValidationError

from src.db_lib.base.exceptions import NotFoundInDBError

from src.backend.core.utils import crud
from src.backend.core.decorators import login_jwt_required_decorator
from src.backend.core.response.schemas import ErrorMessageSchema
from src.backend.settings import USER_MODEL
from src.backend.core.exceptions import ForbiddenError


from .schemas import CategoryInSchema, CategoryOutSchema, CategoryAllOutSchema
from .models import Category


class CategoriesMethodView(MethodView):

    @login_jwt_required_decorator
    def get(self, current_user: USER_MODEL) -> tuple[Response, int]:
        return jsonify(CategoryAllOutSchema(categories=current_user.profile.categories).model_dump()), 200

    @login_jwt_required_decorator
    def post(self, current_user: USER_MODEL) -> tuple[Response, int]:
        try:
            new_category_data = request.get_json()
            new_category_validated = CategoryInSchema(**new_category_data)
            new_category_validated.profile_id = current_user.profile.id
            new_category_model = Category(**new_category_validated.model_dump())
            new_category = crud.create(new_category_model)
        except ValidationError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 400
        else:
            return jsonify(CategoryOutSchema.model_validate(new_category)), 201


class CategoriesByIDMethodView(MethodView):

    @login_jwt_required_decorator
    def get(self, current_user: USER_MODEL, category_id: int) -> tuple[Response, int]:
        try:
            category = crud.read(Category, pk=category_id)
            if category.profile_id != current_user.profile.id:
                raise ForbiddenError()
        except ForbiddenError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 403
        except NotFoundInDBError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 404
        else:
            return jsonify(CategoryOutSchema.model_validate(category)), 200

    @login_jwt_required_decorator
    def put(self, current_user: USER_MODEL, category_id: int) -> tuple[Response, int]:
        try:
            old_category = crud.read(Category, pk=category_id)
            if old_category.profile_id != current_user.profile.id:
                raise ForbiddenError()
            update_category_data = request.get_json()
            update_category_validated = CategoryInSchema(**update_category_data)
            update_category_validated.profile_id = current_user.profile.id
            update_category = crud.update(
                model=Category,
                pk=old_category.id,
                obj_data=update_category_validated.model_dump(),
            )
        except ValidationError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 400
        except ForbiddenError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 403
        except NotFoundInDBError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 404
        else:
            return jsonify(CategoryOutSchema.model_validate(update_category)), 200

    @login_jwt_required_decorator
    def delete(self, current_user: USER_MODEL, category_id: int) -> tuple[Response, int]:
        try:
            old_category = crud.read(Category, pk=category_id)
            if old_category.profile_id != current_user.profile.id:
                raise ForbiddenError()
            crud.delete(Category, pk=old_category.id)
        except ForbiddenError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 403
        except NotFoundInDBError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 404
        else:
            return jsonify(), 204
