# A marks namespace
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields


marks_ns = Namespace("marks", description="A namespace for marks")

marks_model = marks_ns.model(
    "Marks",
    {
        "id": fields.Integer(),
        "subject": fields.String(),
        "score": fields.Integer(),
        "teacher_id":fields.Integer(),
        "student_id": fields.Integer()
    }
)
