from flask import Blueprint, jsonify, request
from models.database import db
from models.order import Order
from datetime import datetime

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

@order_routes.route("/orders", methods=["POST"])
def create_order():
    """
    Create a new order
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - customer_name
            - total_amount
          properties:
            customer_name:
              type: string
            total_amount:
              type: number
            status:
              type: string
              enum: [pending, processing, shipped, delivered, cancelled]
    responses:
      201:
        description: Order created successfully
      400:
        description: Invalid input
    """
    data = request.get_json()
    
    if not data.get("customer_name"):
        return jsonify({"error": "Customer name is required"}), 400
    
    if not data.get("total_amount") and data.get("total_amount") != 0:
        return jsonify({"error": "Total amount is required"}), 400
    
    new_order = Order(
        customer_name=data["customer_name"],
        order_date=datetime.utcnow(),
        total_amount=float(data["total_amount"]),
        status=data.get("status", "pending")
    )
    
    db.session.add(new_order)
    db.session.commit()
    
    return jsonify(new_order.to_dict()), 201

@order_routes.route("/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    """
    Update an order by ID
    ---
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: ID of the order to update
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            customer_name:
              type: string
            total_amount:
              type: number
            status:
              type: string
              enum: [pending, processing, shipped, delivered, cancelled]
    responses:
      200:
        description: Order updated successfully
      404:
        description: Order not found
      400:
        description: Invalid input
    """
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    data = request.get_json()
    
    if "customer_name" in data:
        order.customer_name = data["customer_name"]
    if "total_amount" in data:
        order.total_amount = float(data["total_amount"])
    if "status" in data:
        order.status = data["status"]
    
    db.session.commit()
    
    return jsonify(order.to_dict()), 200