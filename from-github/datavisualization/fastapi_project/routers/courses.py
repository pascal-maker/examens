from typing import List
from fastapi import APIRouter, HTTPException, status
from models.course import Course
import json

# Create a router object
# This lets us put all course routes together in one file
router = APIRouter()

# Open the JSON file and load all courses into the courses list
with open("data/courses.json", "r") as file:
    courses = json.load(file)

# Function to save the current courses list back to the JSON file
def save_courses():
    with open("data/courses.json", "w") as file:
        json.dump(courses, file, indent=4)

# GET route to return all courses
@router.get(
    "/mct/courses",
    tags=["Course"],
    response_model=List[Course],
    summary="Return all courses"
)
def getAllCourses():
    # Convert every dictionary in the courses list into a Course object
    return list(map(lambda course: Course(**course), courses))

# GET route to return all courses for a specific track
@router.get(
    "/mct/courses/track/{track}",
    tags=["Course"],
    response_model=List[Course],
    summary="Return all courses by track"
)
def getAllCoursesByTrack(track: str):
    # Keep only the courses where:
    # - tracks is None
    # OR
    # - the given track is inside the tracks list
    filtered = filter(
        lambda course: course["tracks"] is None or track in course["tracks"],
        courses
    )

    # Convert the filtered dictionaries into Course objects
    return list(map(lambda course: Course(**course), filtered))

# GET route to return courses with a specific name
@router.get(
    "/mct/courses/name/{name}",
    tags=["Course"],
    response_model=List[Course],
    summary="Return all courses by name"
)
def getCourseByName(name: str):
    # Keep only the courses whose title matches the given name
    filtered = filter(lambda course: course["title"] == name, courses)

    # Convert the filtered dictionaries into Course objects
    return list(map(lambda course: Course(**course), filtered))

# POST route to create a new course
@router.post(
    "/mct/courses",
    tags=["Course"],
    response_model=Course,
    status_code=status.HTTP_201_CREATED
)
def create_course(course: Course):
    # Convert the Course object to a dictionary and add it to the list
    courses.append(course.model_dump())

    # Save the updated list to the JSON file
    save_courses()

    # Return the created course
    return course

# PUT route to update an existing course by index
@router.put(
    "/mct/courses/{course_id}",
    response_model=Course,
    tags=["Course"]
)
def update_course(course_id: int, update_course: Course):
    # Check if the index exists
    if course_id < 0 or course_id >= len(courses):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    # Replace the old course with the new updated course
    courses[course_id] = update_course.model_dump()

    # Save the updated list
    save_courses()

    # Return the updated course
    return update_course

# DELETE route to remove a course by index
@router.delete("/mct/courses/{course_id}", tags=["Course"])
def delete_course(course_id: int):
    # Check if the index exists
    if course_id < 0 or course_id >= len(courses):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    # Remove the course from the list
    deleted = courses.pop(course_id)

    # Save the updated list
    save_courses()

    # Return a success message
    return {"message": f"Course {deleted['title']} deleted successfully"}