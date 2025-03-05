from flask import Blueprint, jsonify
from models.database import db
from models.facture import Facture

facture_routes = Blueprint("facture_routes", __name__)

@facture_routes.route("/factures", methods=["GET"])
def get_products():
    """
    Toute les factures
    ---
    responses:
      200: description: De toutes les factures dans la base de données
    """
    facture = Facture.query.all()
    return jsonify([product.to_dict() for product in facture]), 200

@facture_routes.route("/factures/<int:facture_id>", methods=["GET"])
def get_facture(facture_id):
    """
    Retrieve a facture by ID
    ---
    parameters:
      - name: facture_id
        in: path
        type: integer
        required: true
        description: ID of the facture to retrieve
    responses:
      200:
        description: Facture details
      404:
        description: Facture not found
    """
    facture = Facture.query.get(facture_id)
    if facture:
        return jsonify(facture.to_dict()), 200
    return jsonify({"error": "Facture not found"}), 404