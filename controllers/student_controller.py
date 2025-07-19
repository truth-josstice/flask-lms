from flask import Blueprint, jsonify, request
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
@student_bp.route("/", methods=["POST"])
def create_a_student():
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

# PUT/PATCH /id
# DELETE /id