from typing import List
from fastapi import APIRouter, HTTPException, status
from models.student import Student
import json

# Create a router object
# This groups all student routes together in one file
router = APIRouter()

# Open the students JSON file and load all student data into a list
with open("data/students.json", "r") as file:
    students = json.load(file)

# Function to save the current students list back to the JSON file
def save_students():
    with open("data/students.json", "w") as file:
        json.dump(students, file, indent=4)

# GET route to return all students
@router.get(
    "/mct/students",
    tags=["Student"],
    response_model=List[Student],
    summary="Return all students"
)
def getAllStudents():
    # Convert every dictionary in the students list into a Student object
    return list(map(lambda student: Student(**student), students))

# GET route to return all students for a specific track
@router.get(
    "/mct/students/track/{track}",
    tags=["Student"],
    response_model=List[Student],
    summary="Return all students by track"
)
def getStudentByTrack(track: str):
    # Keep only the students whose track matches the given track
    filtered = filter(lambda student: student["track"] == track, students)

    # Convert the filtered dictionaries into Student objects
    return list(map(lambda student: Student(**student), filtered))

# GET route to return all students with a specific name
@router.get(
    "/mct/students/name/{name}",
    tags=["Student"],
    response_model=List[Student],
    summary="Return all students by name"
)
def getStudentByName(name: str):
    # Keep only the students whose name matches the given name
    filtered = filter(lambda student: student["name"] == name, students)

    # Convert the filtered dictionaries into Student objects
    return list(map(lambda student: Student(**student), filtered))

# POST route to create a new student
@router.post(
    "/mct/students",
    tags=["Student"],
    response_model=Student,
    status_code=status.HTTP_201_CREATED
)
def create_student(student: Student):
    # Convert the Student object into a dictionary and add it to the list
    students.append(student.model_dump())

    # Save the updated students list to the JSON file
    save_students()

    # Return the newly created student
    return student

# DELETE route to remove a student by index
@router.delete("/mct/students/{student_id}", tags=["Student"])
def delete_student(student_id: int):
    # Check if the student index exists in the list
    if student_id < 0 or student_id >= len(students):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    # Remove the student from the list
    deleted = students.pop(student_id)

    # Save the updated students list
    save_students()

    # Return a success message
    return {"message": f"Student {deleted['name']} deleted successfully"}