import unittest
from app import create_app
from models.database import db
from models.product import Product

class ProductTestCase(unittest.TestCase):
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

    def test_get_products_empty(self):
        """Test retrieving products when the database is empty"""
        response = self.client.get("/api/products")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_get_products(self):
        """Test retrieving products with data in the database"""
        with self.app.app_context():
            product = Product(name="Test Product", description="This is a test product", price=19.99)
            db.session.add(product)
            db.session.commit()

        response = self.client.get("/api/products")
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["name"], "Test Product")
        self.assertEqual(response.json[0]["description"], "This is a test product")
        self.assertEqual(response.json[0]["price"], 19.99)

if __name__ == "__main__":
    unittest.main()