from flask import Blueprint, jsonify
from init import db
from models.student import Student, students_schema, student_schema

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

    if data:
        # student_json = [student["name"] for student in data]
        # print(student_json)

        # student_python_obj = [student.name for student in students_list]
        # print(student_python_obj)
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
# PUT/PATCH /id
# DELETE /id