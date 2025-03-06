import unittest
from app import create_app
from models.database import db
from models.order import Order
from datetime import datetime

class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_orders_empty(self):
        """Test retrieving orders when the database is empty"""
        response = self.client.get("/api/orders")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_get_orders(self):
        """Test retrieving orders with data in the database"""
        with self.app.app_context():
            order1 = Order(
                customer_name="John Doe",
                order_date=datetime(2025, 2, 1),
                total_amount=99.99,
                status="completed"
            )
            order2 = Order(
                customer_name="Jane Smith",
                order_date=datetime(2025, 2, 15),
                total_amount=149.99,
                status="pending"
            )
            db.session.add(order1)
            db.session.add(order2)
            db.session.commit()

        response = self.client.get("/api/orders")
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(len(response.json), 2)
        
        self.assertEqual(response.json[0]["customer_name"], "John Doe")
        self.assertEqual(response.json[0]["total_amount"], 99.99)
        self.assertEqual(response.json[0]["status"], "completed")
        
        self.assertEqual(response.json[1]["customer_name"], "Jane Smith")
        self.assertEqual(response.json[1]["total_amount"], 149.99)
        self.assertEqual(response.json[1]["status"], "pending")

if __name__ == "__main__":
    unittest.main()
