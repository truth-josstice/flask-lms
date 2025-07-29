from init import db

class Teacher(db.Model):
    # Name of the table
    __tablename__ = "teachers"

    # Attributes
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(150))

    courses = db.relationship("Course", back_populates="teacher")