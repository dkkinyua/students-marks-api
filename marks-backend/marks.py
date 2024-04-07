# A marks namespace
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from model import Mark
from extensions import db

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

@marks_ns.route("/hello")
class HelloResource(Resource):
    def get(self):
        message = {
            "message": "Hello World"
        }
        return message
    
@marks_ns.route("/marks")
class MarksResource(Resource):
    @marks_ns.marshal_list_with(marks_model)
    def get(self):
        marks = Mark.query.get()

        return marks
    
    @marks_ns.marshal_with(marks_model)
    def post(self):
        data = request.get_json()
        new_marks = Mark(
            subject = data.get("subject"),
            score = data.get("score"),
            student_id = data.get("student_id"),
            teacher_id = data.get("teacher_id")
        )           
    
        new_marks.save()
        return jsonify({
            "message": "Marks recorded."
        })