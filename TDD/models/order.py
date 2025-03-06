from models.database import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending")

    def to_dict(self):
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "order_date": self.order_date.isoformat(),
            "total_amount": self.total_amount,
            "status": self.status
        }