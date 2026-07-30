from pydantic import BaseModel

class Lecturer(BaseModel):
    name: str
    language: str
    track: str
    programmingLanguage: str
    favouriteCourse: str

    def sayHello(self):
        print(f"Hello, my name is {self.name} and I love {self.favouriteCourse}")
