from flask import Blueprint, jsonify, request
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

@product_routes.route("/products", methods=["POST"])
def create_product():
    """
    Create a new product
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - price
          properties:
            name:
              type: string
            description:
              type: string
            price:
              type: number
    responses:
      201:
        description: Product created successfully
      400:
        description: Invalid input
    """
    data = request.get_json()
    
    # Validate required fields
    if not data.get("name"):
        return jsonify({"error": "Name is required"}), 400
    
    if not data.get("price") and data.get("price") != 0:
        return jsonify({"error": "Price is required"}), 400
    
    # Create new product
    new_product = Product(
        name=data["name"],
        description=data.get("description", ""),
        price=float(data["price"])
    )
    
    # Save to database
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify(new_product.to_dict()), 201