from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

# Create an engine
engine = create_engine('postgresql://postgres:<password>@localhost:5432/python')

# Create a session factory
Session = sessionmaker(bind=engine)

# Create a base class for declarative models
Base = declarative_base()


# Define the model class for the "students" table
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    grade = Column(Integer)


# Create (INSERT) route
@app.route('/students', methods=['POST'])
def create_student():
    session = Session()
    data = request.json
    student = Student(name=data['name'], age=data['age'], grade=data['grade'])
    session.add(student)
    session.commit()
    return jsonify({'id': student.id})


# Read (SELECT) route
@app.route('/students', methods=['GET'])
def get_students():
    session = Session()
    students = session.query(Student).all()
    student_list = []
    for student in students:
        student_list.append({
            'id': student.id,
            'name': student.name,
            'age': student.age,
            'grade': student.grade
        })
    return jsonify(student_list)


@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    session = Session()
    student = session.query(Student).get(student_id)
    if student:
        return jsonify({
            'id': student.id,
            'name': student.name,
            'age': student.age,
            'grade': student.grade
        })
    else:
        return jsonify({'message': f'Student not found with id= {student_id}'}), 404


# Update (UPDATE) route
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    session = Session()
    student = session.query(Student).get(student_id)
    data = request.json
    if 'name' in data:
        student.name = data['name']
    if 'age' in data:
        student.age = data['age']
    if 'grade' in data:
        student.grade = data['grade']
    session.commit()
    return jsonify(student)


# Delete (DELETE) route
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    session = Session()
    student = session.query(Student).get(student_id)
    session.delete(student)
    session.commit()
    return jsonify({'message': 'Student deleted successfully'})


if __name__ == '__main__':
    app.debug = True
    app.run(port=8080)
