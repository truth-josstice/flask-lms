from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Related, RelatedList, Nested
from marshmallow import fields, ValidationError, validates
from marshmallow.validate import Range, OneOf


from models.student import Student
from models.teacher import Teacher
from models.course import Course

from models.enrolment import Enrolment


class StudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True
        include_relationships = True
        ordered=True
        fields= ("id", "name", "email", "address", "enrolments")

    enrolments = RelatedList(Nested("EnrolmentSchema", only=("id", "enrolment_date", "course")))


class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        load_instance = True
        include_fk = True
        include_relationships = True
        fields = ("id", "name", "department", "address", "courses")
        ordered = True

    courses = RelatedList(Nested("CourseSchema", exclude=("teacher","id")))
    department = auto_field(validate=OneOf(
        choices=["Management", "Science", "Engineering"],
        error = "Only valid departments are: Management, Science or Engineering."
        ))



class CourseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Course
        load_instance = True
        include_fk = True
        include_relationships = True
        ordered = True

        fields = ("id","name","duration", "teacher", "enrolments")

    duration = auto_field(validate=[
        Range(min=1, error="Duration value must be at least 1.")
    ])

    #validation functions
    #@validates("property-to-validate")
    #def some_function_name(self, property-to-validate, data_key)

    @validates("name")
    def validates_name(self, name, data_key):
        if len(name) < 2:
            print("Course name is too short!")
            raise ValidationError("Course name is too short!")

    teacher = Nested("TeacherSchema", only=("id","name","department"))
    enrolments = RelatedList(Nested("EnrolmentSchema", exclude=("course",)))

	
class EnrolmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Enrolment
        load_instance = True
        include_fk = True
        include_relationships = True
        ordered=True
        fields=("id", "enrolment_date", "student", "course")
    
    student = Nested("StudentSchema", only=("id", "name"))
    course = Nested("CourseSchema", only=("id", "name"))

    
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

enrolment_schema = EnrolmentSchema()
enrolments_schema = EnrolmentSchema(many=True)

