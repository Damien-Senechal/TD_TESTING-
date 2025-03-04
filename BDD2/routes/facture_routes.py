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