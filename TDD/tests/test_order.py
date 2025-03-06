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
        # Add some orders to the database
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

        # Retrieve all orders
        response = self.client.get("/api/orders")
        self.assertEqual(response.status_code, 200)
        
        # Verify response contains the added orders
        self.assertEqual(len(response.json), 2)
        
        # Verify first order
        self.assertEqual(response.json[0]["customer_name"], "John Doe")
        self.assertEqual(response.json[0]["total_amount"], 99.99)
        self.assertEqual(response.json[0]["status"], "completed")
        
        # Verify second order
        self.assertEqual(response.json[1]["customer_name"], "Jane Smith")
        self.assertEqual(response.json[1]["total_amount"], 149.99)
        self.assertEqual(response.json[1]["status"], "pending")
        
    def test_get_order_by_id(self):
        """Test retrieving a single order by ID"""
        # Add an order to the database
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

        # Retrieve the order by ID
        response = self.client.get(f"/api/orders/{order_id}")
        self.assertEqual(response.status_code, 200)
        
        # Verify response contains the correct order
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
        
        # Verify response contains the created order
        self.assertEqual(response.json["customer_name"], "New Customer")
        self.assertEqual(response.json["total_amount"], 199.99)
        self.assertEqual(response.json["status"], "pending")
        self.assertIn("order_date", response.json)
        
        # Verify order was added to the database
        with self.app.app_context():
            order = Order.query.filter_by(customer_name="New Customer").first()
            self.assertIsNotNone(order)
            self.assertEqual(order.total_amount, 199.99)
            
    def test_create_order_missing_fields(self):
        """Test creating an order with missing required fields"""
        # Missing customer_name
        order_data = {
            "total_amount": 199.99,
            "status": "pending"
        }
        response = self.client.post("/api/orders", json=order_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)
        
        # Missing total_amount
        order_data = {
            "customer_name": "Missing Amount Customer",
            "status": "pending"
        }
        response = self.client.post("/api/orders", json=order_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)
        
    def test_update_order_valid(self):
        """Test updating an order with valid data"""
        # First, add an order to the database
        with self.app.app_context():
            order = Order(
                customer_name="Original Customer",
                order_date=datetime(2025, 3, 1),
                total_amount=100.00,
                status="pending"
            )
            db.session.add(order)
            db.session.commit()
            order_id = order.id
        
        # Update the order
        update_data = {
            "customer_name": "Updated Customer",
            "status": "shipped"
        }
        response = self.client.put(f"/api/orders/{order_id}", json=update_data)
        self.assertEqual(response.status_code, 200)
        
        # Verify response contains updated data
        self.assertEqual(response.json["customer_name"], "Updated Customer")
        self.assertEqual(response.json["status"], "shipped")
        # Total amount should remain unchanged
        self.assertEqual(response.json["total_amount"], 100.00)
        
        # Verify order was updated in the database
        with self.app.app_context():
            updated_order = Order.query.get(order_id)
            self.assertEqual(updated_order.customer_name, "Updated Customer")
            self.assertEqual(updated_order.status, "shipped")
            self.assertEqual(updated_order.total_amount, 100.00)
    
    def test_update_order_not_found(self):
        """Test updating an order that doesn't exist"""
        update_data = {
            "customer_name": "Updated Nonexistent Order",
            "status": "cancelled"
        }
        response = self.client.put("/api/orders/999", json=update_data)
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json)
        
    def test_delete_order_valid(self):
        """Test deleting an order that exists"""
        # First, add an order to the database
        with self.app.app_context():
            order = Order(
                customer_name="Customer to Delete",
                order_date=datetime(2025, 3, 5),
                total_amount=75.50,
                status="pending"
            )
            db.session.add(order)
            db.session.commit()
            order_id = order.id
        
        # Delete the order
        response = self.client.delete(f"/api/orders/{order_id}")
        self.assertEqual(response.status_code, 200)
        
        # Verify response contains confirmation message
        self.assertIn("message", response.json)
        self.assertIn("deleted", response.json["message"].lower())
        
        # Verify order was deleted from the database
        with self.app.app_context():
            deleted_order = Order.query.get(order_id)
            self.assertIsNone(deleted_order)
    
    def test_delete_order_not_found(self):
        """Test deleting an order that doesn't exist"""
        response = self.client.delete("/api/orders/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json)

if __name__ == "__main__":
    unittest.main()