from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.enrolment import Enrolment
from schemas.schemas import enrolment_schema, enrolments_schema

enrolment_bp = Blueprint("enrolment", __name__, url_prefix="/enrolments")

@enrolment_bp.route("/")
def get_enrolments():
    course_id = request.args.get("course_id", type=int)
    student_id = request.args.get("student_id", type=int)

    stmt = db.select(Enrolment)

    if course_id:
        stmt = stmt.where(Enrolment.course_id == course_id)

    if student_id:
        stmt = stmt.where(Enrolment.student_id == student_id)
     
    enrolments_list = db.session.scalars(stmt) # Python object
    data = enrolments_schema.dump(enrolments_list) # JavaScript JSON object

    if data:
        return jsonify(data)

    else:
        return {"message": "No enrolment records found."}, 404

@enrolment_bp.route('/<int:enrolment_id>')
def get_an_enrolment(enrolment_id):
    stmt = db.select(Enrolment).where(Enrolment.id == enrolment_id)
    enrolment = db.session.scalar(stmt)

    if enrolment:
        return jsonify(enrolment_schema.dump(enrolment))
    else:
        return {"message": f'Enrolment with id {enrolment_id} does not exist.'}, 404
    
@enrolment_bp.route('/', methods=["POST"])
def create_an_enrolment():
    try:
        body_data = request.get_json()

        new_enrolment = Enrolment(
            student_id = body_data.get("student_id"),
            course_id = body_data.get("course_id"),
            enrolment_date = body_data.get("enrolment_date")
        )

        db.session.add(new_enrolment)
        db.session.commit()

        return jsonify(enrolment_schema.dump(new_enrolment)), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"Required field {err.orig.diag.column_name} cannot be null."}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": err.orig.diag.message_detail}, 400
    
@enrolment_bp.route('/<int:enrolment_id>', methods = ["DELETE"])
def delete_enrolment(enrolment_id):
    stmt = db.select(Enrolment).where(Enrolment.id==enrolment_id)
    enrolment = db.session.scalar(stmt)

    if enrolment:
        db.session.delete(enrolment)
        db.session.commit()

        return {"message": f"Enrolment '{enrolment.name}' has been removed successfully."}, 200
    
    else:
        return {"message": f"Enrolment with id {enrolment_id} does not exist."}, 404

@enrolment_bp.route('/<int:enrolment_id>', methods = ["PUT", "PATCH"])
def update_enrolment(enrolment_id):
    stmt = db.select(Enrolment).where(Enrolment.id==enrolment_id)
    enrolment = db.session.scalar(stmt)

    if enrolment:
        body_data = request.get_json()

        enrolment.enrolment_date = body_data.get("enrolment_date", enrolment.enrolment_date)
        enrolment.student_id = body_data.get("student_id", enrolment.student_id)
        enrolment.course_id = body_data.get("course_id", enrolment.course_id)

        db.session.commit()

        return jsonify(enrolment_schema.dump(enrolment))

    else:
        return {"message": f"Enrolment with id {enrolment_id} does not exist."}, 404