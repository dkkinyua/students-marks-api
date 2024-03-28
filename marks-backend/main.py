from flask import request, jsonify, Flask
from flask_restx import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
api = Api(app, doc="/docs")

@api.route("/hello")
class HelloResource(Resource):
    def get(self):
        message = {
            "message": "Success!"
        }

        return message


if __name__ == "__main__":
    app.run()