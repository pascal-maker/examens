from typing import List, Optional
from pydantic import BaseModel

class Course(BaseModel):
    title: str
    content: str
    semester: int
    pillar: str
    tags: List[str]
    tracks: Optional[List[str]] = None
    lecturers: Optional[List[str]] = None
    students: Optional[List[str]] = None

    def showLecturers(self):
        print(f"The Lecturers for the {self.title} course are {self.lecturers}")
