from flask import Blueprint

from .views import CategoriesByIDMethodView, CategoriesMethodView

categories_bp: Blueprint = Blueprint("categories", __name__)

categories_bp.add_url_rule("/<int:category_id/>", view_func=CategoriesByIDMethodView.as_view("categories_by_id"))
categories_bp.add_url_rule("/", view_func=CategoriesMethodView.as_view("categories"))
