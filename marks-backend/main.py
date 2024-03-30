from flask import request, jsonify, Flask
from flask_restx import Api, Resource, fields
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from config import DevelopmentConfig
from model import Mark, Student, Teacher, db


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
api = Api(app, doc="/docs")
db.init_app(app)
JWTManager(app)
migrate = Migrate(app, db)

# Models {Serialized}
student_model = api.model(
    "Students",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "email": fields.String(),
        "password": fields.String()
    }
)

login_model = api.model(
    "Login", 
    {
        "name": fields.Integer(),
        "password": fields.Integer()
    }
)

teacher_model = api.model(
    "Teachers",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "email": fields.String(),
        "password": fields.String()
    }
)

marks_model = api.model(
    "Marks",
    {
        "id": fields.Integer(),
        "subject": fields.String(),
        "score": fields.Integer(),
        "teacher_id":fields.Integer(),
        "student_id": fields.Integer()
    }
)

@api.route("/hello")
class HelloResource(Resource):
    def get(self):
        message = {
            "message": "Success!"
        }

        return message

@api.route("/marks")
class MarksResource(Resource):
    @api.marshal_list_with(marks_model)
    @jwt_required()
    def get(self):
        marks = Mark.query.all()
        return marks
    
    @api.expect(marks_model)
    @api.marshal_with(marks_model)
    @jwt_required()
    def post(self):
        data = request.get_json()
        new_marks = Mark(
            subject = data.get("subject"),
            score = data.get("score"),
            teacher_id = data.get("teacher_id"),
            student_id = data.get("student_id")
        )
        new_marks.save()
        return new_marks

# A route to get marks by id
@api.route("/mark/<int:id>")
class MarkResource(Resource):
    @api.marshal_with(marks_model)
    @jwt_required()
    def get(self, id):
        marks = Mark.query.get_or_404(id)
        return marks
    
    @api.marshal_with(marks_model)
    @jwt_required()
    def put(self, id):
        data = request.get_json()
        update_marks = Mark.query.get_or_404(id)
        update_marks.update(
            subject = data.get("subject"),
            score = data.get("score")
        )

        return update_marks
    
    @jwt_required()
    def delete(self, id):
        delete_marks = Mark.query.get_or_404(id)
        delete_marks.delete()

        return jsonify(
            {
                "message": "This subject has been deleted!"
            }
        )
    
# Signup Route
@api.route("/signup", methods=["POST"])
class SignupResource(Resource):
    @api.expect(student_model)
    def post(self):
        data = request.get_json()
        name = data.get("name")
        db_name = Student.query.filter_by(name=name).first()

        if db_name is not None:
            return jsonify({
                "message": "This user exists"
            })
        
        new_student = Student(
            name = data.get("name"),
            email = data.get("email"),
            password = generate_password_hash(data.get("password"))
        )

        new_student.save()
        return jsonify({
            "message": f"User {name} has been created."
        })

# Login Route
@api.route("/login", methods=["POST"])
class LoginResource(Resource):
    @api.expect(login_model)
    def post(self):
        data = request.get_json()
        name = data.get("name")
        password = data.get("password")
        db_student = Student.query.filter_by(name=name).first()

        if db_student and check_password_hash(db_student.password, password):
            access_token = create_access_token(identity=db_student.name)
            refresh_token = create_refresh_token(identity=db_student.name)

            return jsonify({
                "message": f"Successfully logged in as {db_student.name}",
                "access_token": access_token,
                "refresh_token": refresh_token
            }) 
    
# Shell Configuration
@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Marks": Mark
    }   


if __name__ == "__main__":
    app.run()