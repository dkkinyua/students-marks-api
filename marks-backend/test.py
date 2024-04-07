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

    # Test: Student Signup route
    def test_student_signup(self):
        test_user = {
            "name": "testuser",
            "email": "testuser@skuli.com",
            "password": "testuser1"
        }

        signup_response = self.client.post("/auth/signup/student", json=test_user)

        status_code = signup_response.status_code

        self.assertEqual(status_code, 201)

    def test_teacher_signup(self):
        test_user = {
            "name": "testuser",
            "email": "testuser@skuli.com",
            "password": "testuser1"
        }
        signup_response = self.client.post("/auth/signup/teacher", json=test_user)
        status_code = signup_response.status_code

        self.assertEqual(status_code, 201)

    def test_student_login(self):
        signup_response = self.client.post("/auth/signup/student", json = {
            "name": "testuser",
            "email": "testuser@skuli.com",
            "password": "testuser1"
        })

        test_user = {
            "name": "testuser",
            "password": "testuser1"
        }

        login_response = self.client.post("/auth/login/student", json=test_user)
        status_code = login_response.status_code

        self.assertEqual(status_code, 200)

    def test_teacher_login(self):
        signup_response = self.client.post("/auth/signup/teacher", json = {
            "name": "testuser",
            "email": "testuser@skuli.com",
            "password": "testuser1"
        })

        test_user = {
            "name": "testuser",
            "password": "testuser1"
        }
        
        login_response = self.client.post("/auth/login/teacher", json=test_user)
        status_code = login_response.status_code

        self.assertEqual(status_code, 200)

    # Gets all subjects and scores
    def test_all_scores(self):
        get_response = self.client.get("/marks/marks")

        status_code = get_response.status_code

        self.assertEqual(status_code, 200)

    # Tear down db after tests
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()