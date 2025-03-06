from flask import Blueprint, jsonify
from models.database import db
from models.order import Order

order_routes = Blueprint("order_routes", __name__)

@order_routes.route("/orders", methods=["GET"])
def get_orders():
    """
    Retrieve all orders
    ---
    responses:
      200:
        description: A list of orders
    """
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders]), 200