import unittest
from app import create_app
from models.database import db
from models.order import Order
from datetime import datetime

class OrderTestCase(unittest.TestCase):
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
        
    def test_get_order_by_id(self):
        """Test retrieving a single order by ID"""
        with self.app.app_context():
            order = Order(
                customer_name="Test Customer",
                order_date=datetime(2025, 3, 1),
                total_amount=125.50,
                status="shipped"
            )
            db.session.add(order)
            db.session.commit()
            order_id = order.id

        response = self.client.get(f"/api/orders/{order_id}")
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.json["id"], order_id)
        self.assertEqual(response.json["customer_name"], "Test Customer")
        self.assertEqual(response.json["total_amount"], 125.50)
        self.assertEqual(response.json["status"], "shipped")
        
    def test_get_order_not_found(self):
        """Test retrieving an order with an ID that doesn't exist"""
        response = self.client.get("/api/orders/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json)
        self.assertEqual(response.json["error"], "Order not found")
        
    def test_create_order_valid(self):
        """Test creating an order with valid data"""
        order_data = {
            "customer_name": "New Customer",
            "total_amount": 199.99,
            "status": "pending"
        }
        response = self.client.post("/api/orders", json=order_data)
        self.assertEqual(response.status_code, 201)
        
        self.assertEqual(response.json["customer_name"], "New Customer")
        self.assertEqual(response.json["total_amount"], 199.99)
        self.assertEqual(response.json["status"], "pending")
        self.assertIn("order_date", response.json)
        
        with self.app.app_context():
            order = Order.query.filter_by(customer_name="New Customer").first()
            self.assertIsNotNone(order)
            self.assertEqual(order.total_amount, 199.99)
            
    def test_create_order_missing_fields(self):
        """Test creating an order with missing required fields"""
        order_data = {
            "total_amount": 199.99,
            "status": "pending"
        }
        response = self.client.post("/api/orders", json=order_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)
        
        order_data = {
            "customer_name": "Missing Amount Customer",
            "status": "pending"
        }
        response = self.client.post("/api/orders", json=order_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

if __name__ == "__main__":
    unittest.main()