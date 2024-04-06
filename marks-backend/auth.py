# A namespace for user authentication
from flask import request, jsonify, make_response
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
        name = data.get("name")
        db_student = Student.query.filter_by(name=name).first()

        if db_student is not None:
            return jsonify({
                "message": f"{name} exists!"
            })
        new_student = Student(
            name=data.get("name"),
            email=data.get("email"),
            password=generate_password_hash(data.get("password"))
        )

        new_student.save()
        return make_response(jsonify({
            "message": f"Student {name} has been created"
        }), 201)
