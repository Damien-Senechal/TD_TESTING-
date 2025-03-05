import unittest
from datetime import datetime
import sys
import os



sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from app import create_app
from models.facture import Facture
from models.database import db

class FactureTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()  
        self.app.config.from_object("config.TestConfig")
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def test_get_factures(self):
        with self.app.app_context():
            facture = Facture(
                id=1,
                nom_client="Test facture",
                montant=19.99,
                date=datetime.strptime("2021-01-01", "%Y-%m-%d").date(),  
                status="En attente"
            )
            db.session.add(facture)
            db.session.commit()

        response = self.client.get("/api/factures")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["id"], 1)
        self.assertEqual(response.json[0]["nom_client"], "Test facture")
        self.assertEqual(response.json[0]["montant"], 19.99)

        
        response_date = response.json[0]["date"]
        formatted_date = datetime.strptime(response_date, "%a, %d %b %Y %H:%M:%S GMT").strftime("%Y-%m-%d")
        self.assertEqual(formatted_date, "2021-01-01")

        self.assertEqual(response.json[0]["status"], "En attente")

    def test_get_facture(self):
        """Test pour récupérer une seule facture par ID"""
        with self.app.app_context():
            facture = Facture(
                nom_client="Client B",
                montant=200.50,
                date=datetime.strptime("2023-06-01", "%Y-%m-%d").date(),
                status="Validée"
            )
            db.session.add(facture)
            db.session.commit()
            facture_id = facture.id

        response = self.client.get(f"/api/factures/{facture_id}")
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertEqual(response_data["nom_client"], "Client B")
        self.assertEqual(response_data["montant"], 200.50)
        self.assertEqual(response_data["status"], "Validée")

