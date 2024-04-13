from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from model import Mark, Student, Teacher
from extensions import db
from marks import marks_ns
from auth import auth_ns

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    CORS(app)
    
    db.init_app(app)
    JWTManager(app)
    migrate = Migrate(app, db)

    api = Api(app, doc="/docs")

    api.add_namespace(marks_ns)
    api.add_namespace(auth_ns)


    # Shell Configuration
    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "Marks": Mark,
            "Student": Student,
            "Teacher": Teacher
        }   

    return app