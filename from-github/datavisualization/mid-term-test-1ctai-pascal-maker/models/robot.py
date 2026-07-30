from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from models.functionality import Functionality, FunctionalityRead


class RobotBase(SQLModel):
    name: str = Field(min_length=1)
    location: Optional[str] = None
    ip_address: Optional[str] = Field(default=None, unique=True)


class Robot(RobotBase, table=True):
    __tablename__ = "robots"
    id: Optional[int] = Field(default=None, primary_key=True)
    current_functionality_id: Optional[int] = Field(
        default=None,
        foreign_key="functionalities.id",
        ondelete="SET NULL",
    )
    functionality: Optional[Functionality] = Relationship()


class RobotCreate(RobotBase):
    current_functionality_id: Optional[int] = None


class RobotUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=1)
    location: Optional[str] = None
    ip_address: Optional[str] = None
    current_functionality_id: Optional[int] = None


class RobotRead(RobotBase):
    id: int
    current_functionality_id: Optional[int] = None


class RobotReadWithFunctionality(RobotRead):
    functionality: Optional[FunctionalityRead] = None
