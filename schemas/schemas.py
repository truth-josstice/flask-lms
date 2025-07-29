from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from marshmallow_sqlalchemy.fields import Related, RelatedList
from marshmallow.validate import Length, And, Regexp


from models.student import Student
from models.teacher import Teacher
from models.course import Course
from models.enrollment import Enrollment

class StudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True
    
    enrollments = RelatedList(Related(["id", "enrollment_date", "course_id"]))

class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        load_instance = True
        include_fk = True
        include_relationships = True
        fields = ("id", "name", "department", "address", "courses")
        ordered = True

    courses = RelatedList(Related(["name", "duration"]))


class CourseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Course
        load_instance = True
        include_fk = True
        include_relationships = True
        ordered = True
        fields = ("id","name","duration", "teacher")

    enrollments = RelatedList(Related(["id", "enrollment_date", "student_id"]))  
	# name = fields.String(required=True, validate=And(
	# 	Length(min=2, error="Course names must be at least 2 characters long."),
	# 	Regexp("[A-Za-z][A-Za-z0-9 ]*$", error="Only letters, numbers, and spaces are allowed!")
	# ))

	# duration = fields.Float(allow_nan=False, required=False)
	
    teacher = Related(["id","name","department"])


class EnrollmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Enrollment
        load_instance = True
        include_relationships = True
        include_FK = True

    student = Related("id", "name")
    courses = RelatedList(Related(["id", "name"]))

# Student Schema for converting a single entry
student_schema = StudentSchema()

# Student Schema for converting multiple entries
students_schema = StudentSchema(many=True)

# Teacher Schema for converting a single entry
teacher_schema = TeacherSchema()

# Teacher Schema for converting multiple entries
teachers_schema = TeacherSchema(many=True)

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)

enrollment_schema = EnrollmentSchema()
enrollments_schema = EnrollmentSchema(many=True)
