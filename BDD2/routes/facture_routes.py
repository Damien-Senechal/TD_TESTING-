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

@facture_routes.route("/factures", methods=["POST"])
def create_facture():
    """Endpoint to create a new facture."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    new_facture = Facture(
        nom_client=data["nom_client"],
        montant=data["montant"],
        date=data["date"],
        status=data["status"]
    )

    db.session.add(new_facture)
    db.session.commit()

    return jsonify({
        "id": new_facture.id,
        "nom_client": new_facture.nom_client,
        "montant": new_facture.montant,
        "date": new_facture.date,
        "status": new_facture.status
    }), 201