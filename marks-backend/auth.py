# A namespace for user authentication
from flask import request
from flask_restx import Resource, Namespace, fields
from werkzeug.security import check_password_hash, generate_password_hash
from model import Student, Teacher

auth_ns = Namespace("auth", description="A namespace for student and teacher authentication")

student_model = auth_ns.model(
    "Student",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "email": fields.String(),
        "password": fields.String()
    }
)

teacher_model = auth_ns.model(
    "Teacher",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "email": fields.String(),
        "password": fields.String()
    }
)

login_model = auth_ns.model(
    "Login",
    {
        "name": fields.String(),
        "password": fields.String()
    }
)

@auth_ns.route("/signup", methods=["POST"])
class StudentSignupResource(Resource):
    @auth_ns.expect(student_model)
    def post(self):
        data = request.get_json()
