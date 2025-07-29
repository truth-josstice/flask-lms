from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.student import Student
from schemas.schemas import student_schema, students_schema

student_bp = Blueprint("student", __name__, url_prefix="/students")

# Routes
# GET /students/
@student_bp.route("/")
def get_students():
    # Define the GET statement
    # SELECT * FROM student;
    stmt = db.select(Student)
    students_list = db.session.scalars(stmt) # Python object
    data = students_schema.dump(students_list) # JavaScript JSON object

    # For understanding Python objects and JSON objects
    # students_list_a = list(db.session.scalars(stmt))
    # print([student.name for student in students_list_a])
    # student_json = [student["name"] for student in data]
    # print(student_json)
    if data:
        return jsonify(data)
    else:
        return {"message": "No student records found."}, 404


# GET /id
@student_bp.route("/<int:student_id>")
def get_a_student(student_id):
    # Define a statement
    stmt = db.select(Student).where(Student.id == student_id)
    # Execute it
    student = db.session.scalar(stmt)

    if student:
        # Serialise it
        data = student_schema.dump(student)
        # Return the data
        return jsonify(data)
    else:
        return {"message": f"Student with id {student_id} does not exist."}, 404

# POST /
@student_bp.route("/", methods=["POST"])
def create_a_student():
    try:
        # GET info from the REQUEST body
        body_data = request.get_json()

        # Create a Student Object from Student class with body response data
        new_student = Student(
            name = body_data.get("name"),
            email = body_data.get("email"),
            address = body_data.get("address")
        )

        # Add the new student data to the session
        db.session.add(new_student)
        
        # Commit the session
        db.session.commit()

        # Return
        return jsonify(student_schema.dump(new_student)), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"Required field {err.orig.diag.column_name} cannot be null."}, 400
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "Email has to be unique"}, 400
        else:
            return {"message": "Unexpected error occured."}, 400

# DELETE /id
@student_bp.route("/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    # Find the student with the student_id
    stmt = db.select(Student).where(Student.id == student_id)
    student = db.session.scalar(stmt)
    # if exists
    if student:
        # delete the student entry
        db.session.delete(student)
        db.session.commit()

        return {"message": f"Student '{student.name}' has been removed successfully."}, 200
    # else:
    else:
        # return an acknowledgement message
        return {"message": f"Student with id '{student_id}' does not exist"}, 404
    
# UPDATE /students/id
@student_bp.route("/<int:student_id>", methods=["PUT", "PATCH"])
def update_student(student_id):
    # Get the student with id
    stmt = db.select(Student).where(Student.id == student_id)
    student = db.session.scalar(stmt)
    # if exists
    if student:
        # get the data to be updated
        body_data = request.get_json()
        # make changes
        student.name = body_data.get("name") or student.name
        student.email = body_data.get("email") or student.email
        student.address = body_data.get("address") or student.address
        # commit
        db.session.commit()
        # return
        return jsonify(student_schema.dump(student))
    # else
    else:
        # return with an error message
        return {"message": f"Student with id {student_id} does not exist."}, 404