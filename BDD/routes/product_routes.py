from flask import Blueprint, jsonify
from models.database import db
from models.product import Product

product_routes = Blueprint("product_routes", __name__)

@product_routes.route("/products", methods=["GET"])
def get_products():
    """
    Retrieve all products
    ---
    responses:
      200:
        description: A list of products
    """
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products]), 200