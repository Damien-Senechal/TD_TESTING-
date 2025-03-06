from models.database import db
from sqlalchemy import Date


class Facture(db.Model):
    __tablename__ = "factures"
    

    id = db.Column(db.Integer, primary_key=True)
    nom_client = db.Column(db.String(100), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(10), nullable=False)  
    status = db.Column(db.String(20), nullable=False)


    def to_dict(self):
        return {
            "id": self.id,
            "nom_client": self.nom_client,
            "montant": self.montant,
            "date": self.date,
            "status": self.status
        }
