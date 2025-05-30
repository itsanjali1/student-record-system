from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

# MySQL DB connection via SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:anjali@localhost/student_record_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(20), nullable=False)

    grades = db.relationship('Grade', backref='student', lazy=True)
    attendances = db.relationship('Attendance', backref='student', lazy=True)

# Subject Model
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(20), nullable=False)

    grades = db.relationship('Grade', backref='subject', lazy=True)
    attendances = db.relationship('Attendance', backref='subject', lazy=True)

# Grade Model
class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    grade = db.Column(db.Float, nullable=False)

# Attendance Model
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    total_classes = db.Column(db.Integer, nullable=False)
    attended_classes = db.Column(db.Integer, nullable=False)

# Create tables
with app.app_context():
    db.create_all()
