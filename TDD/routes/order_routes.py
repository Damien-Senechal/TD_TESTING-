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

@order_routes.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    """
    Retrieve an order by ID
    ---
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: ID of the order to retrieve
    responses:
      200:
        description: Order details
      404:
        description: Order not found
    """
    order = Order.query.get(order_id)
    if order:
        return jsonify(order.to_dict()), 200
    return jsonify({"error": "Order not found"}), 404