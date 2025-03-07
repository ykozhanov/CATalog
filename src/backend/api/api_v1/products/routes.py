from flask import Blueprint

from .views import ProductsMethodView, ProductsByIDMethodView

products_bp: Blueprint = Blueprint("products", __name__)

products_bp.add_url_rule("/<int:product_id>/", view_func=ProductsByIDMethodView.as_view("products_by_id"))
products_bp.add_url_rule("/", view_func=ProductsMethodView.as_view("products"))
