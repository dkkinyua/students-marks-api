# A namespace for user authentication
from flask import request, jsonify, make_response
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
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

#Student Signup route
@auth_ns.route("/signup/student", methods=["POST"])
class StudentSignupResource(Resource):
    @auth_ns.expect(student_model)
    def post(self):
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        db_student = Student.query.filter_by(name=name).first()
        db_email = Student.query.filter_by(email=email).first()

        if db_student is not None:
            return jsonify({
                "message": f"{name} exists!"
            })
        
        if db_email is not None:
             return jsonify({
                "message": f"{email} exists!"
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
    
# Teacher Signup Route
@auth_ns.route("/signup/teacher", methods=["POST"])
class TeacherSignupResource(Resource):
    @auth_ns.expect(teacher_model)
    def post(self):
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        db_teacher = Teacher.query.filter_by(name=name).first()
        db_email = Teacher.query.filter_by(email=email).first()

        if db_teacher is not None:
            return jsonify({
                "message": f"{name} exists!"
            })
        
        if db_email is not None:
            return jsonify({
                "message": f"{email} exists!"
            })
        
        
        new_teacher = Teacher(
            name=data.get("name"),
            email=data.get("email"),
            password=generate_password_hash(data.get("password"))
        )

        new_teacher.save()
        return make_response(jsonify({
            "message": f"Teacher {name} has been created"
        }), 201)
    
#Student Login Route
@auth_ns.route("/login/student", methods=["POST"])
class StudentLoginRoute(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()
        name = data.get("name")
        password = data.get("password")

        db_student = Student.query.filter_by(name=name).first()
        if db_student and check_password_hash(db_student.password, password):
            return jsonify({
                "message": "User logged in."
            })
        
# Teacher Login Route
@auth_ns.route("/login/teacher", methods=["POST"])
class TeacherLoginRoute(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()
        name = data.get("name")
        password = data.get("password")

        db_teacher = Teacher.query.filter_by(name=name).first()
        if db_teacher and check_password_hash(db_teacher.password, password):
            access_token = create_access_token(identity=db_teacher.name)
            refresh_token = create_refresh_token(identity=db_teacher.name)

            return jsonify({
                "message": "Teacher logged in",
                "access_token": access_token,
                "refresh_token": refresh_token
            })

@auth_ns.route("/refresh")
class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)

        return make_response(jsonify({
            "Authorization": f"Bearer {new_access_token}"
        }), 200)