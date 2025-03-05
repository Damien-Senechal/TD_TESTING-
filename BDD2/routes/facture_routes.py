from flask import Blueprint, jsonify, request
from datetime import datetime
import sys
import os
from models.database import db
from models.facture import Facture
from sqlalchemy.orm import Session

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
    


    session: Session = db.session 
    facture = session.get(Facture, facture_id)
    if facture:
        return jsonify(facture.to_dict()), 200
    return jsonify({"error": "Facture not found"}), 404

@facture_routes.route("/api/factures", methods=["POST"])
def create_facture():
    data = request.get_json()

    
    if not all(k in data for k in ("nom_client", "montant", "date", "status")):
        return jsonify({"error": "Données incomplètes"}), 400

    try:
        nouvelle_facture = Facture(
            nom_client=data["nom_client"],
            montant=float(data["montant"]),
            date=datetime.strptime(data["date"], "%Y-%m-%d").date(),
            status=data["status"]
        )
        db.session.add(nouvelle_facture)
        db.session.commit()
        return jsonify(nouvelle_facture.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500