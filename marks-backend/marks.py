# A marks namespace
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
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
        marks = Mark.query.all()

        return marks
    
    @marks_ns.expect(marks_model)
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

# Getting, Updating and Deleting marks by id 
@marks_ns.route("/mark/<int:id>")
class MarkResource(Resource):
    @marks_ns.marshal_with(marks_model)
    @jwt_required()
    def get(self, id):
        marks = Mark.query.get_or_404(id)
        return marks
    
    @marks_ns.expect(marks_model)
    @marks_ns.marshal_with(marks_model)
    @jwt_required()
    def put(self, id):
        data = request.get_json()
        marks_to_update = Mark.query.get_or_404(id)
        marks_to_update.update(
            subject = data.get("subject"),
            score = data.get("score")
        )
        return marks_to_update
    
    @jwt_required()
    def delete(self, id):
        marks_to_delete = Mark.query.get_or_404(id)
        marks_to_delete.delete()

        return jsonify(
            {
                "message": "Subject and score deleted"
            }
        )

