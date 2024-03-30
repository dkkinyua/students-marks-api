from flask import request, jsonify, Flask
from flask_restx import Api, Resource, fields
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
from flask_migrate import Migrate
from config import DevelopmentConfig
from model import Mark, Student, Teacher, db

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
api = Api(app, doc="/docs")
db.init_app(app)
migrate = Migrate(app, db)

# Models {Serialized}
student_model = api.model(
    "Students",
    {
        "id": fields.Integer(),
        "username": fields.String(),
        "email": fields.String(),
        "password": fields.String()
    }
)

teacher_model = api.model(
    "Teachers",
    {
        "id": fields.Integer(),
        "username": fields.String(),
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
    def get(self):
        marks = Mark.query.all()
        return marks
    
    @api.expect(marks_model)
    @api.marshal_with(marks_model)
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
    def get(self, id):
        marks = Mark.query.get_or_404(id)
        return marks
    
    @api.marshal_with(marks_model)
    def put(self, id):
        data = request.get_json()
        update_marks = Mark.query.get_or_404(id)
        update_marks.update(
            subject = data.get("subject"),
            score = data.get("score")
        )

        return update_marks
    
    def delete(self, id):
        delete_marks = Mark.query.get_or_404(id)
        delete_marks.delete()

        return jsonify(
            {
                "message": "This subject has been deleted!"
            }
        )
# Shell Configuration

@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Marks": Mark
    }   


if __name__ == "__main__":
    app.run()