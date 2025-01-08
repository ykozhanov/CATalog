from flask import jsonify, Response
from flask.views import MethodView

from src.db_lib.base.exceptions import NotFoundInDBError
from src.backend.core.mixins import HashPWMixin, JWTWithGetTokenMixin
from src.backend.core.decorators import base64_login_decorator, get_jwt_token_decorator, base64_register_decorator
from src.backend.core.utils import crud
from src.backend.core.response import ErrorMessageSchema
from src.backend.core.request import TYPE_REFRESH_JWT
from src.backend.core.database.schemas import LoginSchema, RegisterSchema
from src.backend.core.exceptions import AuthenticationError
from src.backend.core.exceptions.messages import MESSAGE_REGISTER_ERROR_401

from src.backend.settings import USER_MODEL
from .schemas import TokensSchema
from .models import Profile


class LoginMethodView(MethodView, HashPWMixin, JWTWithGetTokenMixin):
    """Обрабатывает вход пользователя и генерацию access и refresh JWT токенов.

    Методы:
        post(login_data: LoginSchema) -> tuple[Response, int]:
            Аутентифицирует пользователя и возвращает access и refresh токены.
    """

    @base64_login_decorator
    def post(self, login_data: LoginSchema) -> tuple[Response, int]:
        """Аутентифицирует пользователя с предоставленными данными для входа.

        Аргументы:
            login_data (LoginSchema): Данные для входа, содержащие имя пользователя и пароль.

        Возвращает:
            tuple[Response, int]: Кортеж, содержащий JSON-ответ с токенами и HTTP статус-код.
                - В случае успеха: (JSON с access и refresh токенами, 200)
                - В случае ошибки: (JSON с сообщением об ошибке, 401)
        """
        try:
            user = crud.where(model=USER_MODEL, attr="username", content=login_data.username)[0]
            if not user or not self._check_hashpw(password=login_data.password, hashed_password=user.password):
                raise AuthenticationError()
            refresh_token = self._get_jwt_token(sub=user.id)
            access_token = self._get_jwt_token(refresh_token=refresh_token)
            crud.update(model=Profile, pk=user.profile.id, obj_data={"refresh_token": refresh_token})
        except (AuthenticationError, NotFoundInDBError) as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 401
        else:
            return jsonify(TokensSchema(access_token=access_token, refresh_token=refresh_token).model_dump()), 200


class RegisterMethodView(MethodView, HashPWMixin, JWTWithGetTokenMixin):
    """Обрабатывает регистрацию пользователя и генерацию access и refresh JWT токенов.

    Методы:
        post(register_data: RegisterSchema) -> tuple[Response, int]:
            Регистрирует нового пользователя и возвращает access и refresh токены.
    """

    @base64_register_decorator
    def post(self, register_data: RegisterSchema) -> tuple[Response, int]:
        """Регистрирует нового пользователя с предоставленными данными для регистрации.

        Аргументы:
            register_data (RegisterSchema): Данные для регистрации, содержащие имя пользователя, пароль и email.

        Возвращает:
            tuple[Response, int]: Кортеж, содержащий JSON-ответ с токенами и HTTP статус-код.
                - В случае успеха: (JSON с access и refresh токенами, 201)
                - В случае ошибки: (JSON с сообщением об ошибке, 401)
        """
        try:
            user = crud.where(model=USER_MODEL, attr="username", content=register_data.username)[0]
            if user:
                raise AuthenticationError(f"{MESSAGE_REGISTER_ERROR_401}: Пользователь с таким username уже существует")
            new_user = USER_MODEL(register_data.model_dump())
            new_user_with_id = crud.create(obj=new_user)
            refresh_token = self._get_jwt_token(sub=new_user_with_id.id)
            jwt_token_model = Profile(refresh_token=refresh_token, user_id=new_user_with_id.id)
            crud.create(obj=jwt_token_model)
            access_token = self._get_jwt_token(refresh_token=refresh_token, message=MESSAGE_REGISTER_ERROR_401)
            return jsonify(TokensSchema(access_token=access_token, refresh_token=refresh_token).model_dump()), 201

        except AuthenticationError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 401


class TokenMethodView(MethodView, JWTWithGetTokenMixin):
    """Обрабатывает генерацию access JWT токена на основе refresh токена.

    Методы:
        post(refresh_token: str) -> tuple[Response, int]:
            Обновляет access токен с использованием refresh токена.
    """

    @get_jwt_token_decorator(type_token=TYPE_REFRESH_JWT)
    def post(self, refresh_token: str) -> tuple[Response, int]:
        """Обновляет access токен с использованием предоставленного refresh токена.

        Аргументы:
            refresh_token (str): Refresh токен для обновления access токена.

        Возвращает:
            tuple[Response, int]: Кортеж, содержащий JSON-ответ с токенами и HTTP статус-код.
                - В случае успеха: (JSON с access и refresh токенами, 200)
                - В случае ошибки: (JSON с сообщением об ошибке, 401)
        """
        try:
            access_token = self._get_jwt_token(refresh_token=refresh_token)
        except AuthenticationError as e:
            return jsonify(ErrorMessageSchema(message=str(e)).model_dump()), 401
        return jsonify(TokensSchema(access_token=access_token, refresh_token=refresh_token).model_dump()), 200
