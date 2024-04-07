import unittest
from config import TestConfig
from main import create_app
from extensions import db


class APITestCase(unittest.TestCase):
    # Sets up the test db
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    # First test ("/marks/hello")
    def test_hello(self):
        hello_response = self.client.get("/marks/hello")

        json = hello_response.json

        self.assertEqual(json, {"message": "Hello World"})

    # Tear down db after tests
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        