from typing import List
from fastapi import APIRouter, HTTPException, status
from models.lecturer import Lecturer
import json

# Create a router object
# This groups all lecturer routes together
router = APIRouter()

# Open the lecturers JSON file and load all lecturer data into a list
with open("data/lecturers.json", "r") as file:
    lecturers = json.load(file)

# Function to save the current lecturers list back to the JSON file
def save_lecturers():
    with open("data/lecturers.json", "w") as file:
        json.dump(lecturers, file, indent=4)

# GET route to return all lecturers
@router.get(
    "/mct/lecturers",
    tags=["Lecturer"],
    response_model=List[Lecturer],
    summary="Return all lecturers"
)
def getAllLecturers():
    # Convert every dictionary in the lecturers list into a Lecturer object
    return list(map(lambda lecturer: Lecturer(**lecturer), lecturers))

# GET route to return lecturers with a specific name
@router.get(
    "/mct/lecturers/name/{name}",
    tags=["Lecturer"],
    response_model=List[Lecturer],
    summary="Return all lecturers by name"
)
def getLecturerByName(name: str):
    # Keep only the lecturers whose name matches the given name
    filtered = filter(lambda lecturer: lecturer["name"] == name, lecturers)

    # Convert the filtered dictionaries into Lecturer objects
    return list(map(lambda lecturer: Lecturer(**lecturer), filtered))

# GET route to return lecturers for a specific track
@router.get(
    "/mct/lecturers/track/{track}",
    tags=["Lecturer"],
    response_model=List[Lecturer],
    summary="Return all lecturers by track"
)
def getLecturerByTrack(track: str):
    # Keep only the lecturers whose track matches the given track
    filtered = filter(lambda lecturer: lecturer["track"] == track, lecturers)

    # Convert the filtered dictionaries into Lecturer objects
    return list(map(lambda lecturer: Lecturer(**lecturer), filtered))

# POST route to create a new lecturer
@router.post(
    "/mct/lecturers",
    tags=["Lecturer"],
    response_model=Lecturer,
    status_code=status.HTTP_201_CREATED
)
def create_lecturer(lecturer: Lecturer):
    # Convert the Lecturer object into a dictionary and add it to the list
    lecturers.append(lecturer.model_dump())

    # Save the updated lecturers list to the JSON file
    save_lecturers()

    # Return the newly created lecturer
    return lecturer

# DELETE route to remove a lecturer by index
@router.delete("/mct/lecturers/{lecturer_id}", tags=["Lecturer"])
def delete_lecturer(lecturer_id: int):
    # Check if the lecturer index exists in the list
    if lecturer_id < 0 or lecturer_id >= len(lecturers):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lecturer not found"
        )

    # Remove the lecturer from the list
    deleted = lecturers.pop(lecturer_id)

    # Save the updated lecturers list
    save_lecturers()

    # Return a success message
    return {"message": f"Lecturer {deleted['name']} deleted successfully"}