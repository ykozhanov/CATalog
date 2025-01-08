from flask import Blueprint

from .views import LoginMethodView, RegisterMethodView, TokenMethodView

auth_bp: Blueprint = Blueprint("auth", __name__)

auth_bp.add_url_rule("/login/", view_func=LoginMethodView.as_view("login"), methods=["POST"])
auth_bp.add_url_rule("/register/", view_func=RegisterMethodView.as_view("register"), methods=["POST"])
auth_bp.add_url_rule("/token/", view_func=TokenMethodView.as_view("token"), methods=["POST"])
