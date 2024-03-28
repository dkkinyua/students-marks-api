from flask import request, jsonify, Flask
from flask_restx import Api, Resource, fields
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
api = Api(app, doc="/docs")

# Models {Serialized}
student_model = api.models(
    "Students",
    {
        "id": fields.Integer(),
        "username": fields.String(),
        "email": fields.String(),
        "password": fields.String()
    }
)

teacher_model = api.models(
    "Teachers",
    {
        "id": fields.Integer(),
        "username": fields.String(),
        "email": fields.String(),
        "password": fields.String()
    }
)

marks_model = api.models(
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


if __name__ == "__main__":
    app.run()