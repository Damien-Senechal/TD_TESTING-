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
        # First, add a product to the database
        with self.app.app_context():
            product = Product(name="Test Product", description="This is a test product", price=19.99)
            db.session.add(product)
            db.session.commit()

        # Then retrieve all products
        response = self.client.get("/api/products")
        self.assertEqual(response.status_code, 200)
        
        # Verify response contains the added product
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["name"], "Test Product")
        self.assertEqual(response.json[0]["description"], "This is a test product")
        self.assertEqual(response.json[0]["price"], 19.99)
        
    def test_get_product_by_id(self):
        """Test retrieving a product by its ID"""
        # First, add a product to the database
        with self.app.app_context():
            product = Product(name="Test Product", description="This is a test product", price=19.99)
            db.session.add(product)
            db.session.commit()
            product_id = product.id

        # Then retrieve the product by ID
        response = self.client.get(f"/api/products/{product_id}")
        self.assertEqual(response.status_code, 200)
        
        # Verify response contains the correct product
        self.assertEqual(response.json["name"], "Test Product")
        self.assertEqual(response.json["description"], "This is a test product")
        self.assertEqual(response.json["price"], 19.99)
        
    def test_get_product_not_found(self):
        """Test retrieving a product with an ID that doesn't exist"""
        response = self.client.get("/api/products/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json)
        self.assertEqual(response.json["error"], "Product not found")
        
    def test_create_product_valid(self):
        """Test creating a product with valid data"""
        product_data = {
            "name": "New Product",
            "description": "This is a new product",
            "price": 29.99
        }
        response = self.client.post("/api/products", json=product_data)
        self.assertEqual(response.status_code, 201)
        
        # Verify response contains the created product
        self.assertEqual(response.json["name"], "New Product")
        self.assertEqual(response.json["description"], "This is a new product")
        self.assertEqual(response.json["price"], 29.99)
        
        # Verify product was added to the database
        with self.app.app_context():
            product = Product.query.filter_by(name="New Product").first()
            self.assertIsNotNone(product)
            self.assertEqual(product.price, 29.99)
            
    def test_create_product_missing_fields(self):
        """Test creating a product with missing required fields"""
        # Missing name
        product_data = {
            "description": "Missing name product",
            "price": 19.99
        }
        response = self.client.post("/api/products", json=product_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)
        
        # Missing price
        product_data = {
            "name": "Missing Price Product",
            "description": "This product has no price"
        }
        response = self.client.post("/api/products", json=product_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

if __name__ == "__main__":
    unittest.main()