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

@product_routes.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """
    Retrieve a product by ID
    ---
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
        description: ID of the product to retrieve
    responses:
      200:
        description: Product details
      404:
        description: Product not found
    """
    product = Product.query.get(product_id)
    if product:
        return jsonify(product.to_dict()), 200
    return jsonify({"error": "Product not found"}), 404