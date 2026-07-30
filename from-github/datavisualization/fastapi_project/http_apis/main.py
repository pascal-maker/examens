import sys
import os

# Add the parent folder to the Python path
# so Python can find the models and routers folders
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Optional and List for type hints
from typing import Optional, List

# Import FastAPI tools
from fastapi import FastAPI, HTTPException, status

# Import Strawberry for GraphQL
import strawberry
from strawberry.fastapi import GraphQLRouter

# -----------------------------
# Import the Pydantic models
# -----------------------------
from models.course import Course
from models.lecturer import Lecturer
from models.student import Student

# -----------------------------
# Import the router files
# Aliases are used so their names
# do not conflict with the data lists
# -----------------------------
from routers import courses as courses_router
from routers import lecturers as lecturers_router
from routers import students as students_router

# -----------------------------
# Import the actual data lists
# and the save functions from each router
# -----------------------------
from routers.courses import courses, save_courses
from routers.lecturers import lecturers, save_lecturers
from routers.students import students, save_students

# Create the FastAPI app
app = FastAPI()

# Add all separate router endpoints to the app
app.include_router(courses_router.router)
app.include_router(lecturers_router.router)
app.include_router(students_router.router)

# -----------------------------
# Basic test route
# -----------------------------
@app.get("/")
def read_root():
    return {"message": "Hello World"}

# -----------------------------
# Another test route with:
# - item_id as path parameter
# - q as optional query parameter
# -----------------------------
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

# ==================================================
# GRAPHQL SETUP
# ==================================================

# Convert the Pydantic Course model
# into a GraphQL type
@strawberry.experimental.pydantic.type(model=Course, all_fields=True)
class CourseType:
    pass

# Convert the Pydantic Lecturer model
# into a GraphQL type
@strawberry.experimental.pydantic.type(model=Lecturer, all_fields=True)
class LecturerType:
    pass

# Convert the Pydantic Student model
# into a GraphQL type
@strawberry.experimental.pydantic.type(model=Student, all_fields=True)
class StudentType:
    pass

# ==================================================
# GRAPHQL QUERIES
# These are used to fetch data
# ==================================================
@strawberry.type
class Query:

    # Return all lecturers
    @strawberry.field
    def lecturers(self) -> List[LecturerType]:
        return list(map(lambda lecturer: Lecturer(**lecturer), lecturers))

    # Return all courses
    @strawberry.field
    def courses(self) -> List[CourseType]:
        return list(map(lambda course: Course(**course), courses))

    # Return all students
    @strawberry.field
    def students(self) -> List[StudentType]:
        return list(map(lambda student: Student(**student), students))

# ==================================================
# GRAPHQL MUTATIONS
# These are used to add/change data
# ==================================================
@strawberry.type
class Mutation:

    # Add a new lecturer
    @strawberry.mutation
    def add_lecturer(
        self,
        name: str,
        language: str,
        track: str,
        programmingLanguage: str,
        favouriteCourse: str
    ) -> LecturerType:

        # Create a Lecturer object
        lecturer = Lecturer(
            name=name,
            language=language,
            track=track,
            programmingLanguage=programmingLanguage,
            favouriteCourse=favouriteCourse
        )

        # Add it to the lecturers list
        lecturers.append(lecturer.model_dump())

        # Save the updated lecturers list
        save_lecturers()

        # Return the new lecturer
        return lecturer

    # Add a new student
    @strawberry.mutation
    def add_student(
        self,
        name: str,
        language: str,
        track: str,
        programmingLanguage: str,
        favouriteCourse: str
    ) -> StudentType:

        # Create a Student object
        student = Student(
            name=name,
            language=language,
            track=track,
            programmingLanguage=programmingLanguage,
            favouriteCourse=favouriteCourse
        )

        # Add it to the students list
        students.append(student.model_dump())

        # Save the updated students list
        save_students()

        # Return the new student
        return student

    # Add a new course
    @strawberry.mutation
    def add_course(
        self,
        title: str,
        content: str,
        semester: int,
        pillar: str,
        tags: List[str]
    ) -> CourseType:

        # Create a Course object
        course = Course(
            title=title,
            content=content,
            semester=semester,
            pillar=pillar,
            tags=tags
        )

        # Add it to the courses list
        courses.append(course.model_dump())

        # Save the updated courses list
        save_courses()

        # Return the new course
        return course

# Create the GraphQL schema using the Query and Mutation classes
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Create the GraphQL router
graphql_app = GraphQLRouter(schema, path="/graphql")

# Add GraphQL to the FastAPI app
app.include_router(graphql_app)